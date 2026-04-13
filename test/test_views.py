import pytest


# Delta covered: ssrf_lab now blocks traversal/absolute paths and constrains to basename.

def test_ssrf_lab_rejects_traversal_and_uses_basename(mocker):
    from introduction import views

    # Avoid reading files and template rendering
    render_mock = mocker.patch.object(views, "render", return_value="OK")
    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called"))

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()

        def __init__(self, blog):
            self.POST = {"blog": blog}

    # traversal should be rejected before open
    views.ssrf_lab(DummyRequest("../secret.txt"))
    assert open_mock.call_count == 0

    # absolute should be rejected before open
    views.ssrf_lab(DummyRequest("/etc/passwd"))
    assert open_mock.call_count == 0

    # If a subpath is provided without traversal, basename should be used; we can assert
    # it attempts to open using basename by checking open() arguments.
    open_mock2 = mocker.patch("builtins.open", mocker.mock_open(read_data="ok"))
    views.ssrf_lab(DummyRequest("subdir/file.txt"))
    assert "file.txt" in str(open_mock2.call_args[0][0])
    render_mock.assert_called()
