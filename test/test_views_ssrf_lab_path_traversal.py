import pytest


def test_ssrf_lab_rejects_absolute_and_parent_traversal_paths(mocker):
    """Regression test: user-controlled file path must be rejected when absolute or contains '..'."""
    # Import inside test so that failures are localized
    from introduction import views

    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "../secrets.txt"}

    render_spy = mocker.patch.object(views, "render", autospec=True)

    views.ssrf_lab(request)

    render_spy.assert_called()
    # Context is the 3rd positional arg: (request, template, context)
    context = render_spy.call_args.args[2]
    assert context == {"blog": "Invalid file path provided"}
