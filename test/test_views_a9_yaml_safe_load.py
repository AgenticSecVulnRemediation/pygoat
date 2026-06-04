import pytest


def test_a9_lab_uses_yaml_safe_load(mocker):
    """Regression test for insecure YAML loading: must call yaml.safe_load, not yaml.load."""
    from introduction import views

    file_obj = mocker.Mock()

    safe_load = mocker.patch.object(views.yaml, "safe_load", autospec=True, return_value={"k": "v"})
    load = mocker.patch.object(views.yaml, "load", autospec=True)
    render_spy = mocker.patch.object(views, "render", autospec=True)

    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.FILES = {"file": file_obj}

    views.a9_lab(request)

    assert safe_load.called
    assert not load.called
    render_spy.assert_called()
