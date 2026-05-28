# Assumption: 'introduction.views' is importable during tests and Django is configured.
# These tests focus ONLY on the security fix: yaml.load(...) -> yaml.safe_load(...)

import io
import types

import pytest

import introduction.views as views


class _User:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


class _Files(dict):
    pass


class _Request:
    def __init__(self, method="POST", authenticated=True, file_bytes=b"a: 1\n"):
        self.method = method
        self.user = _User(authenticated)
        self.FILES = _Files({"file": io.BytesIO(file_bytes)})


def test_a9_lab_uses_yaml_safe_load_instead_of_load(monkeypatch):
    # Arrange
    called = {"safe_load": 0, "load": 0}

    def safe_load_stub(_stream):
        called["safe_load"] += 1
        return {"a": 1}

    def load_stub(*_args, **_kwargs):
        called["load"] += 1
        raise AssertionError("yaml.load must not be used")

    monkeypatch.setattr(views.yaml, "safe_load", safe_load_stub)
    monkeypatch.setattr(views.yaml, "load", load_stub)

    def render_stub(_request, _template, context=None):
        # Return the context so we can assert it without a Django test client.
        return context or {}

    monkeypatch.setattr(views, "render", render_stub)

    request = _Request(file_bytes=b"a: 1\n")

    # Act
    ctx = views.a9_lab(request)

    # Assert
    assert called["safe_load"] == 1
    assert called["load"] == 0
    assert ctx["data"] == {"a": 1}
