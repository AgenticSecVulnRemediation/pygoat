import os

import introduction.views as views


def test_ssrf_lab_normalizes_and_rejects_traversal(monkeypatch):
    # Arrange: make open fail if called (it should not be called for traversal)
    monkeypatch.setattr(views, "open", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("open should not be called")))

    class _Req:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"

        class POST:
            @staticmethod
            def __getitem__(k):
                assert k == "blog"
                return "../secrets.txt"

    # Act
    resp = views.ssrf_lab(_Req())

    # Assert: view should handle invalid path and return a response (we can't easily inspect template context here)
    assert resp is not None
