import importlib
import os
from pathlib import Path


def test_ssrf_lab_blocks_path_traversal_outside_playground_directory(tmp_path, monkeypatch):
    """Regression test for traversal hardening.

    The fix uses realpath + startswith(base_dir) to prevent reading files outside
    the playground directory.
    """

    # Import inside test to avoid import-time binding before monkeypatching __file__
    module = importlib.import_module("introduction.playground.ssrf.main")

    fake_module_file = tmp_path / "pkg" / "main.py"
    fake_module_file.parent.mkdir(parents=True)
    fake_module_file.write_text("# placeholder")

    monkeypatch.setattr(module, "__file__", str(fake_module_file))

    secret_outside = tmp_path / "secret.txt"
    secret_outside.write_text("TOPSECRET")

    # Attempt traversal outside base_dir
    result = module.ssrf_lab("../secret.txt")

    assert result == {"blog": "No blog found"}
