import types

import pytest


# module under test
from introduction import views


def test_ssrf_lab2_blocks_non_allowlisted_domain(mocker):
    """Delta test for SSRF fix: disallow requests to domains not in allowlist."""

    # Build minimal request object used by the view.
    class Req:
        method = "POST"
        POST = {"url": "http://169.254.169.254/latest/meta-data/"}

        class User:
            is_authenticated = True

        user = User()

    render_mock = mocker.patch.object(views, "render", autospec=True)
    get_mock = mocker.patch.object(views.requests, "get", autospec=True)

    views.ssrf_lab2(Req())

    # Should short-circuit before doing the outbound request.
    get_mock.assert_not_called()

    # Should render with an error indicating domain not allowed.
    assert render_mock.call_count == 1
    _, _, kwargs = render_mock.mock_calls[0]
    # render(request, template, context)
    # In autospec=True, first arg is module function, so use call_args instead.
    called_args, _ = render_mock.call_args
    context = called_args[2]
    assert context == {"error": "Domain not allowed"}
