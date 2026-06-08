# Assumption: Django app module is importable as `introduction.views` in test environment.
# This test targets the path traversal mitigation in ssrf_lab: absolute-path + startswith(base+os.sep).

import os
import pytest


def _build_request(blog_value: str, authenticated: bool = True):
    class _User:
        def __init__(self, authed: bool):
            self.is_authenticated = authed

    class _Req:
        def __init__(self, blog: str, authed: bool):
            self.user = _User(authed)
            self.method = "POST"
            self.POST = {"blog": blog}

    return _Req(blog_value, authenticated)


def test_ssrf_lab_rejects_path_traversal_outside_views_dir(mocker, tmp_path):
    """Previously `os.path.join(dirname, file)` permitted '../' traversal.

    After patch, any resolved path not starting with (dirname + os.sep) is rejected.
    We mock __file__-derived dirname by patching introduction.views.__file__.
    """
    import introduction.views as views

    # Arrange: choose a fake views.py location with a safe base directory
    base_dir = tmp_path / "introduction"
    base_dir.mkdir()
    fake_views_py = base_dir / "views.py"
    fake_views_py.write_text("# placeholder")

    # Put a sensitive file outside base_dir
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("TOPSECRET")

    # Patch module __file__ so dirname becomes base_dir
    mocker.patch.object(views, "__file__", str(fake_views_py))

    # Attempt traversal to reach secret_file
    traversal = os.path.join("..", "secret.txt")
    req = _build_request(traversal)

    # Mock render so we can inspect context without needing templates
    render_mock = mocker.patch.object(views, "render", side_effect=lambda req, tpl, ctx=None: {"tpl": tpl, "ctx": ctx})

    # Act
    result = views.ssrf_lab(req)

    # Assert: should fall into except and return "No blog found" rather than reading secret
    assert result["ctx"]["blog"] == "No blog found"
    # Ensure it did not attempt to open the sensitive file
    # (No direct open mock here; rejection happens prior to open, so success path is blocked.)
    render_mock.assert_called()
