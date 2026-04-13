import pytest


# Delta covered: yaml.load(..., yaml.Loader) replaced with yaml.safe_load(file)
# to avoid arbitrary object construction.

def test_a9_lab_uses_yaml_safe_load(mocker):
    from introduction import views

    safe_load_mock = mocker.patch.object(views.yaml, "safe_load", return_value={"k": "v"})

    class DummyUser:
        is_authenticated = True

    class DummyFiles(dict):
        pass

    class DummyRequest:
        method = "POST"
        user = DummyUser()

        def __init__(self):
            self.FILES = DummyFiles(file=mocker.Mock())

    render_mock = mocker.patch.object(views, "render", return_value="OK")

    req = DummyRequest()

    views.a9_lab(req)

    safe_load_mock.assert_called_once_with(req.FILES["file"])
    render_mock.assert_called()
