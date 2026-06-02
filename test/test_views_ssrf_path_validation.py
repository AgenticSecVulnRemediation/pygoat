import os

import pytest


def test_ssrf_lab_blocks_absolute_or_traversal_paths():
    """Regression test for SSRF lab local file inclusion hardening."""
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')

    assert 'os.path.isabs(file) or ..' not in content  # sanity: avoid malformed check
    assert "os.path.isabs(file)" in content
    assert "'..' in file" in content
    assert 'Unauthorized file access attempt detected' in content
