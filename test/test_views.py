import pytest


def test_ssrf_lab2_blocks_non_http_schemes_and_private_hosts(monkeypatch):
    # Arrange
    import introduction.views as views

    class _DummyUser:
        is_authenticated = True

    def fake_render(_request, _template, context=None, **_kwargs):
        return context or {}

    monkeypatch.setattr(views, "render", fake_render)

    # If blocked early, requests.get must not be called.
    monkeypatch.setattr(
        views.requests,
        "get",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("requests.get must not be called")),
    )

    class _ReqFileScheme:
        method = "POST"
        user = _DummyUser()
        POST = {"url": "file:///etc/passwd"}

    class _ReqLoopback:
        method = "POST"
        user = _DummyUser()
        POST = {"url": "http://127.0.0.1/"}

    # Act
    ctx1 = views.ssrf_lab2(_ReqFileScheme())
    ctx2 = views.ssrf_lab2(_ReqLoopback())

    # Assert
    assert ctx1.get("error") == "Invalid or disallowed URL"
    assert ctx2.get("error") == "Invalid or disallowed URL"
