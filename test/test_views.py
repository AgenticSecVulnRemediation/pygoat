import types
import pytest

# Assumptions:
# - Django is available and introduction.views can be imported.
# - We unit-test the changed behavior by asserting path traversal is rejected before open().


def test_ssrf_lab_rejects_path_traversal_via_realpath_prefix_check(mocker):
    # Arrange
    import introduction.views as views

    request = types.SimpleNamespace()
    request.user = types.SimpleNamespace(is_authenticated=True)
    request.method = "POST"
    request.POST = {"blog": "../secret.txt"}

    # Force the computed resolved path to be outside dirname
    mocker.patch.object(views.os.path, "dirname", return_value="/app/introduction")
    mocker.patch.object(views.os.path, "realpath", side_effect=lambda p: "/etc/passwd" if p != "/app/introduction" else "/app/introduction")

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called for invalid path"))
    render_mock = mocker.patch.object(views, "render", return_value="RENDERED")

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    assert resp == "RENDERED"
    open_mock.assert_not_called()
    render_mock.assert_called()
    _, _, ctx = render_mock.mock_calls[0].args
    assert ctx["blog"] == "Invalid path"
