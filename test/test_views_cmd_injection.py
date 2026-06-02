import pytest


def test_cmd_lab_uses_shell_false_and_argument_list():
    """Regression test for command injection fix: ensure subprocess.Popen uses shell=False and argv list."""
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')

    # Expect a list-form command for nslookup/dig and shell=False
    assert "command = ['nslookup', domain]" in content or 'command = ["nslookup", domain]' in content
    assert "command = ['dig', domain]" in content or 'command = ["dig", domain]' in content
    assert 'shell=False' in content
