import os

import pytest


# Import from the module under test
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_and_absolute_paths(tmp_path, monkeypatch):
    """Delta test: after the fix, ssrf_lab must reject traversal/absolute paths."""

    # Ensure the module's __file__ points at a controlled directory so path checks are deterministic.
    # ssrf_lab uses os.path.dirname(__file__).
    fake_module_file = tmp_path / "main.py"
    fake_module_file.write_text("# placeholder")

    import introduction.playground.ssrf.main as ssrf_module

    monkeypatch.setattr(ssrf_module, "__file__", str(fake_module_file))

    # Attempt traversal
    assert ssrf_lab("../secrets.txt") == {"blog": "Invalid file path provided"}

    # Attempt absolute path
    assert ssrf_lab(os.path.abspath(str(tmp_path / "secrets.txt"))) == {"blog": "Invalid file path provided"}
