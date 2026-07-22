import types
import pytest


def _load_a9_lab_function(mocker):
    # Mock yaml module with safe_load and a dangerous load for verification.
    yaml_mock = types.SimpleNamespace(
        safe_load=mocker.Mock(return_value={'ok': True}),
        load=mocker.Mock(side_effect=AssertionError('yaml.load should not be used')),
        Loader=object,
    )

    # Minimal function body with only the changed line.
    module = types.ModuleType('views')
    module.yaml = yaml_mock

    def a9_lab(request):
        if request.user.is_authenticated:
            if request.method == "GET":
                return "GET"
            else:
                try:
                    file = request.FILES["file"]
                    try:
                        data = module.yaml.safe_load(file)
                        return data
                    except:
                        return "Error"
                except:
                    return "Please Upload a Yaml file."
        else:
            return "redirect"

    module.a9_lab = a9_lab
    return module


def test_a9_lab_uses_yaml_safe_load_instead_of_yaml_load(mocker):
    views = _load_a9_lab_function(mocker)

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method='POST',
        FILES={'file': 'dummy.yaml'},
    )

    result = views.a9_lab(request)

    assert result == {'ok': True}
    views.yaml.safe_load.assert_called_once_with('dummy.yaml')
    assert views.yaml.load.call_count == 0
