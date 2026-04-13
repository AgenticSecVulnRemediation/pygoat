import pytest


# Delta covered: ssrf_lab now blocks path traversal (.. or absolute paths).

def test_ssrf_lab_rejects_traversal_and_does_not_open_file(mocker):
    from introduction import views

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called"))
    render_mock = mocker.patch.object(views, "render", return_value="OK")

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()

        def __init__(self, blog):
            self.POST = {"blog": blog}

    req = DummyRequest(blog="../secret.txt")

    views.ssrf_lab(req)

    assert open_mock.call_count == 0
    # Should render with invalid path message
    assert "Invalid file path" in str(render_mock.call_args)
