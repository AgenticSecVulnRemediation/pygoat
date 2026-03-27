import types
import pytest

# Assumptions:
# - Django is available and introduction.views can be imported.
# - We unit-test the changed behavior: non-http(s) or non-allowlisted netloc is blocked before requests.get().


def test_ssrf_lab2_blocks_non_allowlisted_url_before_requests_get(mocker):
    # Arrange
    import introduction.views as views

    request = types.SimpleNamespace()
    request.user = types.SimpleNamespace(is_authenticated=True)
    request.method = "POST"
    request.POST = {"url": "http://127.0.0.1/admin"}

    get_mock = mocker.patch.object(views.requests, "get", side_effect=AssertionError("requests.get must not be called for blocked URL"))
    render_mock = mocker.patch.object(views, "render", return_value="RENDERED")

    # Act
    resp = views.ssrf_lab2(request)

    # Assert
    assert resp == "RENDERED"
    get_mock.assert_not_called()
    _, _, ctx = render_mock.mock_calls[0].args
    assert ctx["error"] == "URL not allowed"
