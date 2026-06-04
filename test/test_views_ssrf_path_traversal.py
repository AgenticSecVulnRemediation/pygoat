import pytest


# Assumption: module path is importable from repo root.
import introduction.views as views


def test_ssrf_lab_blocks_path_traversal_in_blog_parameter(mocker):
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "../../etc/passwd"}

    # Avoid filesystem access; the traversal should be blocked before open() is invoked.
    open_mock = mocker.patch("builtins.open", autospec=True)

    response = views.ssrf_lab(request)

    assert open_mock.call_count == 0
    # We can't easily assert the rendered template context without Django test client;
    # but we can assert we returned some response object.
    assert response is not None
