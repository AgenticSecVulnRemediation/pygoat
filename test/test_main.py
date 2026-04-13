import os

import pytest

# Assumption: module is importable as introduction.playground.ssrf.main
from introduction.playground.ssrf import main


def test_ssrf_lab_rejects_path_traversal_and_returns_no_blog_found(monkeypatch):
    opened = []

    def fake_open(*args, **kwargs):
        opened.append(args[0])
        raise AssertionError("open() should not be called for traversal attempts")

    monkeypatch.setattr(main, "open", fake_open, raising=False)

    res = main.ssrf_lab("../secrets.txt")

    assert res == {"blog": "No blog found"}
    assert opened == []
