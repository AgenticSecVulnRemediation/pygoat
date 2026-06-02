import pytest

import introduction.mitre as mitre


class _FakeProcess:
    def communicate(self):
        stdout = b"STATE SERVICE\n\n22/tcp open ssh\n"
        stderr = b""
        return stdout, stderr


def test_command_out_does_not_invoke_shell(mocker):
    popen = mocker.patch('subprocess.Popen', autospec=True)
    popen.return_value = _FakeProcess()

    mitre.command_out(["echo", "hi"])

    _, called_kwargs = popen.call_args
    # Regression: command_out must not pass shell=True
    assert 'shell' not in called_kwargs or called_kwargs['shell'] is False
