import os

import pytest


# This patch adds path traversal validation to ssrf_lab (Django view).
# We test that traversal attempts are rejected BEFORE any file access occurs.

def test_ssrf_lab_rejects_path_traversal_and_absolute_paths(mocker):
    views = pytest.importorskip("introduction.views")

    # Arrange: ensure open() is never reached on invalid paths
    open_spy = mocker.patch("builtins.open", autospec=True)

    def _render_stub(request, template, context=None):
        # return context for inspection
        return {"template": template, "context": context or {}}

    mocker.patch.object(views, "render", side_effect=_render_stub)

    class _User:
        is_authenticated = True

    class _Req:
        user = _User()
        method = "POST"
        POST = {"blog": "../../etc/passwd"}

    # Act
    resp = views.ssrf_lab(_Req())

    # Assert
    assert resp["template"] == "Lab/ssrf/ssrf_lab.html"
    assert resp["context"]["blog"] == "Invalid file path"
    open_spy.assert_not_called()

    # Absolute path should also be rejected
    _Req.POST = {"blog": os.path.abspath("/etc/passwd")}
    resp2 = views.ssrf_lab(_Req())
    assert resp2["context"]["blog"] == "Invalid file path"
    open_spy.assert_not_called()
