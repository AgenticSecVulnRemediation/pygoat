import os

import pytest


# Assumptions:
# - The project uses pytest.
# - The Django view function is imported directly for unit-level tests.
# - We avoid requiring a full Django test client by stubbing only what is needed.


def _make_authenticated_request(post_dict):
    class _User:
        is_authenticated = True

    class _Req:
        user = _User()
        method = "POST"
        POST = post_dict

    return _Req()


def test_ssrf_lab_blocks_absolute_path_and_parent_traversal(mocker):
    """Regression: ssrf_lab() should reject abs paths / '..' before opening files."""
    from introduction import views

    # Arrange
    render_spy = mocker.patch.object(views, "render", autospec=True)
    open_spy = mocker.patch("builtins.open", autospec=True)

    # Absolute path attempt
    req_abs = _make_authenticated_request({"blog": "/etc/passwd"})

    # Act
    views.ssrf_lab(req_abs)

    # Assert
    open_spy.assert_not_called()
    render_spy.assert_called()
    args, kwargs = render_spy.call_args
    # kwargs may be empty; template context is positional in this codebase
    assert "Invalid file path" in str(args) or "Invalid file path" in str(kwargs)

    render_spy.reset_mock()
    open_spy.reset_mock()

    # Parent traversal attempt
    req_parent = _make_authenticated_request({"blog": "../secrets.txt"})

    # Act
    views.ssrf_lab(req_parent)

    # Assert
    open_spy.assert_not_called()
    render_spy.assert_called()
    args, kwargs = render_spy.call_args
    assert "Invalid file path" in str(args) or "Invalid file path" in str(kwargs)
