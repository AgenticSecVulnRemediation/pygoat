# Assumptions:
# - This repo uses pytest and pytest-mock.


def test_ssrf_lab_rejects_absolute_or_parent_paths_before_open(mocker):
    """Delta: ssrf_lab now rejects traversal/absolute paths using normpath + isabs."""
    from introduction import views

    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "../../etc/passwd"}

    # If old behavior tries to open, fail
    mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))

    sentinel = object()

    def _render(_request, _template, context=None):
        assert context["blog"] == "Invalid file path provided."
        return sentinel

    mocker.patch.object(views, "render", side_effect=_render)

    resp = views.ssrf_lab(request)

    assert resp is sentinel
