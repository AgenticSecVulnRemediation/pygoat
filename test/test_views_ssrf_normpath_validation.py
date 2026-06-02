import pytest


def test_ssrf_lab_rejects_traversal_and_absolute_paths():
    """Regression test for SSRF LFI hardening in views.ssrf_lab."""
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')

    # new guardrails
    assert "'..' in file" in content
    assert 'os.path.isabs(file)' in content
    assert 'os.path.normpath' in content
    assert '.startswith(os.path.abspath(dirname) + os.path.sep)' in content
