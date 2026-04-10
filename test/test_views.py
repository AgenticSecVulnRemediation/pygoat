import importlib


def test_ssrf_lab_returns_invalid_file_path_for_traversal(monkeypatch):
    # Arrange
    views = importlib.import_module('introduction.views')

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"blog": "../secrets.txt"}

    # Patch render to avoid Django template rendering dependency
    def fake_render(_request, _template, context=None):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    result = views.ssrf_lab(DummyRequest())

    # Assert
    assert result == {'blog': 'Invalid file path provided'}
