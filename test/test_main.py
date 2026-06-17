import pytest


def test_ssrf_lab_rejects_absolute_and_parent_paths(tmp_path):
    """Regression test for absolute/.. checks in playground SSRF helper."""

    # Import inside test so it uses repository module layout
    from introduction.playground.ssrf.main import ssrf_lab

    assert ssrf_lab("../secret.txt")["blog"] == "No blog found"

    # Construct an absolute path (platform-independent)
    abs_path = str(tmp_path / "file.txt")
    assert ssrf_lab(abs_path)["blog"] == "No blog found"
