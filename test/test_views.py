import pytest


def test_ssrf_lab_blocks_path_traversal_outside_base_dir(monkeypatch):
    # Arrange
    import introduction.views as views

    class _DummyUser:
        is_authenticated = True

    class _DummyRequest:
        method = "POST"
        user = _DummyUser()
        POST = {"blog": "../views.py"}

    # If blocked early, open must not be called.
    monkeypatch.setattr(
        "builtins.open",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("open() must not be called")),
    )

    # Avoid template rendering dependency; return context for assertions.
    def fake_render(_request, _template, context=None, **_kwargs):
        return context or {}

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    context = views.ssrf_lab(_DummyRequest())

    # Assert
    assert context.get("blog") == "Invalid file path." or context.get("blog") == "Invalid file path."
