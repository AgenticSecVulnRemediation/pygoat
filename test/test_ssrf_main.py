import builtins
import os


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    from introduction.playground.ssrf import main

    def open_fail(*args, **kwargs):
        raise AssertionError("open() should not be called for absolute path")

    monkeypatch.setattr(builtins, "open", open_fail)

    result = main.ssrf_lab(os.path.abspath('/etc/passwd'))
    assert result == {"blog": "Invalid file input"}


def test_ssrf_lab_rejects_parent_traversal(monkeypatch):
    from introduction.playground.ssrf import main

    def open_fail(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal")

    monkeypatch.setattr(builtins, "open", open_fail)

    result = main.ssrf_lab('../secret.txt')
    assert result == {"blog": "Invalid file input"}
