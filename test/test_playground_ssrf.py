import builtins
import pytest


def test_ssrf_playground_blocks_absolute_path(monkeypatch):
    """Regression for ssrf playground: absolute paths should be blocked."""
    from introduction.playground.ssrf import main

    def fail_open(*args, **kwargs):
        raise AssertionError("open should not be called for absolute path")

    monkeypatch.setattr(builtins, "open", fail_open)

    res = main.ssrf_lab("/etc/passwd")
    assert res["blog"] == "No blog found"
