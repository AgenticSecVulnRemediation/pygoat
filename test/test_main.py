import os


def test_ssrf_lab_rejects_abs_and_traversal(monkeypatch):
    """Delta behavior: ssrf_lab rejects abs paths and '..' before joining/opening."""

    from introduction.playground.ssrf import main

    assert main.ssrf_lab('../secret.txt') == {"blog": "Invalid file input"}
    assert main.ssrf_lab(os.path.abspath('/etc/passwd')) == {"blog": "Invalid file input"}
