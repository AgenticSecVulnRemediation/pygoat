import yaml
from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


class _AuthUser:
    is_authenticated = True


class _Request:
    def __init__(self, file_bytes: bytes):
        self.user = _AuthUser()
        self.method = "POST"
        self.FILES = {"file": SimpleUploadedFile("t.yaml", file_bytes)}


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange
    request = _Request(b"a: 1\n")

    # Make yaml.load explode if used, to catch regressions back to unsafe loader.
    def boom_load(*args, **kwargs):
        raise AssertionError("yaml.load should not be used; safe_load is required")

    monkeypatch.setattr(views.yaml, "load", boom_load)

    called = {"safe_load": 0}

    real_safe_load = views.yaml.safe_load

    def spy_safe_load(stream):
        called["safe_load"] += 1
        return real_safe_load(stream)

    monkeypatch.setattr(views.yaml, "safe_load", spy_safe_load)

    # Act
    resp = views.a9_lab(request)

    # Assert
    assert called["safe_load"] == 1
    assert resp.status_code == 200
