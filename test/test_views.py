import importlib


def test_ssrf_lab_rejects_traversal_and_does_not_open(monkeypatch):
    # Arrange
    views = importlib.import_module('introduction.views')

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"blog": "../secrets.txt"}

    def fake_open(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal paths")

    monkeypatch.setattr(views, "open", fake_open, raising=False)

    # Act
    resp = views.ssrf_lab(DummyRequest())

    # Assert
    assert resp.status_code == 200
    assert b"No blog found" in resp.content
