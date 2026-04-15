import io

# Assumptions:
# - Django project uses "introduction.views" module path.
# - Delta: yaml.safe_load is used (no yaml.load).
from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, uploaded_bytes: bytes):
        self.user = _DummyUser()
        self.method = "POST"
        # Django UploadedFile is file-like; BytesIO is sufficient for unit test
        self.FILES = {"file": io.BytesIO(uploaded_bytes)}


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange
    payload = b"!!python/object/apply:os.system ['echo pwned']"
    req = _DummyRequest(payload)

    calls = {"safe": 0}

    def _safe_load(file_obj):
        calls["safe"] += 1
        raise Exception("blocked")

    monkeypatch.setattr(views.yaml, "safe_load", _safe_load)
    monkeypatch.setattr(views.yaml, "load", lambda *a, **k: (_ for _ in ()).throw(AssertionError("yaml.load must not be used")))
    monkeypatch.setattr(views, "render", lambda request, tpl, context=None: {"tpl": tpl, "ctx": context})

    # Act
    resp = views.a9_lab(req)

    # Assert
    assert calls["safe"] == 1
    assert resp["ctx"]["data"] == "Error"
