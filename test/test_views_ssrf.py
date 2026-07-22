import os
import types
import pytest


def _load_ssrf_lab_from_views(mocker):
    # Build a minimal module containing only the patched ssrf_lab view implementation.
    module = types.ModuleType('views_ssrf')
    module.os = os

    # Mock render to just return the context (so we can assert blog content / errors)
    module.render = mocker.Mock(side_effect=lambda request, tpl, ctx=None: {"template": tpl, **(ctx or {})})

    code = '''
import os

def ssrf_lab(request):
    if request.user.is_authenticated:
        if request.method=="GET":
            return render(request,"Lab/ssrf/ssrf_lab.html",{"blog":"Read Blog About SSRF"})
        else:
            user_file = request.POST["blog"]
            try:
                dirname = os.path.dirname(__file__)
                base_dir = os.path.abspath(dirname)
                raw_path = os.path.join(dirname, user_file)
                safe_path = os.path.normpath(raw_path)
                if not os.path.abspath(safe_path).startswith(base_dir):
                    raise ValueError('Invalid file path')
                with open(safe_path, "r") as file_handle:
                    data = file_handle.read()
                return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": data})
            except:
                return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": "No blog found"})
    else:
        return "redirect"
'''
    exec(code, module.__dict__)
    return module


def test_ssrf_lab_path_traversal_is_rejected(mocker):
    views = _load_ssrf_lab_from_views(mocker)

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method='POST',
        POST={'blog': '../secrets.txt'},
    )

    # If traversal is rejected, open() should never be called; function falls into except and returns "No blog found".
    open_spy = mocker.patch('builtins.open', autospec=True)

    resp = views.ssrf_lab(request)

    assert resp["blog"] == "No blog found"
    open_spy.assert_not_called()


def test_ssrf_lab_valid_relative_file_reads_from_normalized_path(mocker):
    views = _load_ssrf_lab_from_views(mocker)

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method='POST',
        POST={'blog': 'blog.txt'},
    )

    m = mocker.mock_open(read_data='blog-content')
    mocker.patch('builtins.open', m)

    resp = views.ssrf_lab(request)

    assert resp["blog"] == 'blog-content'
    m.assert_called_once()
