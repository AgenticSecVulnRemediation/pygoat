# Assumption: file is imported as a module `introduction.playground.ssrf.main`.

import os


def test_ssrf_lab_rejects_parent_traversal_and_does_not_open(monkeypatch):
    """Delta test for path traversal fix.

    Changed behavior:
    - reject absolute paths and any path containing '..'
    - should return fallback response and not attempt file open
    """

    from introduction.playground.ssrf import main

    def _open_should_not_be_called(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal input")

    monkeypatch.setattr(main, "open", _open_should_not_be_called, raising=True)

    assert main.ssrf_lab("../secrets.txt") == {"blog": "No blog found"}


def test_ssrf_lab_rejects_absolute_path_and_does_not_open(monkeypatch):
    from introduction.playground.ssrf import main

    def _open_should_not_be_called(*args, **kwargs):
        raise AssertionError("open() should not be called for absolute path input")

    monkeypatch.setattr(main, "open", _open_should_not_be_called, raising=True)

    abs_path = os.path.abspath("/etc/passwd")
    assert main.ssrf_lab(abs_path) == {"blog": "No blog found"}
