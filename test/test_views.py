import types
from unittest.mock import MagicMock

import pytest

# Assumption: Django app module path is "introduction" and ssrf_lab is importable from introduction.views
from introduction.views import ssrf_lab


def _make_request(post_value: str):
    req = types.SimpleNamespace()
    req.method = "POST"
    req.user = types.SimpleNamespace(is_authenticated=True)
    req.POST = {"blog": post_value}
    return req


def test_ssrf_lab_blocks_path_traversal_via_dotdot(monkeypatch):
    request = _make_request("../secret.txt")

    open_spy = MagicMock()
    monkeypatch.setattr("builtins.open", open_spy)

    response = ssrf_lab(request)

    # The fix returns an "Invalid file path provided" blog response; ensure no file is opened
    open_spy.assert_not_called()


def test_ssrf_lab_blocks_absolute_path(monkeypatch):
    request = _make_request("/etc/passwd")

    open_spy = MagicMock()
    monkeypatch.setattr("builtins.open", open_spy)

    response = ssrf_lab(request)

    open_spy.assert_not_called()
