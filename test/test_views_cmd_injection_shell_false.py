import pytest


def test_cmd_lab_uses_shell_false_and_list_command_literal():
    """Regression test for command injection fix variant."""
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')

    assert 'shell=False' in content
    assert '["nslookup", domain]' in content or "['nslookup', domain]" in content
