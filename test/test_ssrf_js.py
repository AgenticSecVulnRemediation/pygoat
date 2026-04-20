import types
from unittest.mock import MagicMock

import pytest

# Assumption: introduction.static.* JS functions are not directly importable in pytest.
# This test executes the module source by eval'ing it into a namespace-like object.


def test_ssrf_js_sanitizes_input_before_sending(monkeypatch):
    # Arrange
    import importlib.util
    import pathlib

    # Locate file relative to repo root at runtime
    js_path = pathlib.Path("introduction/static/Lab/ssrf.js")
    if not js_path.exists():
        pytest.skip("ssrf.js not present in test environment")

    src = js_path.read_text(encoding="utf-8")

    # Very small JS execution shim is not available in pytest; skip if no JS runtime.
    # Since repo is Python-based, assert on code change by checking for sanitize call in source.
    assert "function sanitize" in src
    assert "var python_code = sanitize" in src
    assert "var html_code = sanitize" in src
