# Assumptions:
# - The project uses pytest.
# - PyYAML is installed.
# - introduction.views.a9_lab reads uploaded file objects via request.FILES["file"].

import io

import pytest
import yaml

from introduction import views


class _Req:
    def __init__(self, file_bytes: bytes):
        self.user = type("U", (), {"is_authenticated": True})()
        self.FILES = {"file": io.BytesIO(file_bytes)}
        self.method = "POST"


def test_a9_lab_uses_safe_load_instead_of_unsafe_load(monkeypatch):
    """Regression test: ensure yaml.safe_load is invoked (not yaml.load with Loader).

    We patch yaml.safe_load to a sentinel and make yaml.load raise if called.
    """

    called = {"safe": 0}

    def _safe_load(file_obj):
        called["safe"] += 1
        return {"ok": True}

    def _unsafe_load(*args, **kwargs):
        raise AssertionError("yaml.load must not be used")

    monkeypatch.setattr(views.yaml, "safe_load", _safe_load)
    monkeypatch.setattr(views.yaml, "load", _unsafe_load)

    # Avoid template rendering.
    monkeypatch.setattr(views, "render", lambda request, tpl, ctx=None: ctx)

    resp_ctx = views.a9_lab(_Req(b"a: 1"))

    assert called["safe"] == 1
    assert resp_ctx["data"] == {"ok": True}
