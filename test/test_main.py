import pytest


def test_ssrf_lab_rejects_absolute_path(tmp_path):
    from introduction.playground.ssrf.main import ssrf_lab

    result = ssrf_lab(str(tmp_path / 'secret.txt'))
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_parent_traversal():
    from introduction.playground.ssrf.main import ssrf_lab

    result = ssrf_lab("../etc/passwd")
    assert result == {"blog": "No blog found"}
