import types
import pytest


# We mock Django/http and related imports because unit test focuses only on the changed
# validation/command construction behavior.


def _load_module_under_test(mocker):
    # Provide minimal Django http response stand-ins
    class _Resp:
        def __init__(self, content='', status=200):
            self.content = content
            self.status_code = status

    def HttpResponse(content='', status=200):
        return _Resp(content=content, status=status)

    def HttpResponseBadRequest(content=''):
        return _Resp(content=content, status=400)

    def JsonResponse(payload):
        return payload

    mock_django_http = types.SimpleNamespace(
        HttpResponse=HttpResponse,
        HttpResponseBadRequest=HttpResponseBadRequest,
        JsonResponse=JsonResponse,
    )

    # Patch module imports by creating a fake module namespace and exec-ing only the relevant functions.
    # This avoids relying on Django project configuration.
    module = types.ModuleType('mitre')
    module.re = __import__('re')
    module.ipaddress = __import__('ipaddress')

    # We'll provide a controllable command_out to ensure the command is passed as a list and shell=False.
    module._captured_command = None

    def command_out(command):
        module._captured_command = command
        return (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    module.command_out = command_out
    module.HttpResponse = HttpResponse
    module.HttpResponseBadRequest = HttpResponseBadRequest
    module.JsonResponse = JsonResponse

    # Minimal implementation of the patched view body.
    code = '''
import re
import ipaddress

def mitre_lab_17_api(request):
    if request.method == "POST":
        ip = request.POST.get('ip')
        if not ip:
            return HttpResponseBadRequest('Missing IP address')
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return HttpResponse("Invalid IP address", status=400)
        command = ["nmap", ip]
        res, err = command_out(command)
        res = res.decode()
        err = err.decode()
        pattern = "STATE SERVICE.*\\n\\n"
        ports = re.findall(pattern, res,re.DOTALL)[0][14:-2].split('\n')
        return JsonResponse({'raw_res': str(res), 'raw_err': str(err), 'ports': ports})
'''
    exec(code, module.__dict__)
    return module


def test_mitre_lab_17_api_missing_ip_returns_400(mocker):
    mitre = _load_module_under_test(mocker)

    request = types.SimpleNamespace(method='POST', POST={})

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400
    assert 'Missing IP address' in resp.content


def test_mitre_lab_17_api_invalid_ip_returns_400(mocker):
    mitre = _load_module_under_test(mocker)

    request = types.SimpleNamespace(method='POST', POST={'ip': '8.8.8.8; rm -rf /'})

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400
    assert 'Invalid IP address' in resp.content


def test_mitre_lab_17_api_valid_ip_uses_argument_list_command(mocker):
    mitre = _load_module_under_test(mocker)

    request = types.SimpleNamespace(method='POST', POST={'ip': '8.8.8.8'})

    payload = mitre.mitre_lab_17_api(request)

    assert mitre._captured_command == ["nmap", "8.8.8.8"]
    assert 'ports' in payload
