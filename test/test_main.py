import builtins
import pytest


def test_ssrf_lab_rejects_absolute_path_and_traversal(mocker):
    # Import function under test
    from introduction.playground.ssrf.main import ssrf_lab

    # Absolute path should be rejected
    assert ssrf_lab('/etc/passwd') == {"blog": "Invalid file path detected"}

    # Traversal should be rejected
    assert ssrf_lab('../secrets.txt') == {"blog": "Invalid file path detected"}


def test_ssrf_lab_allows_relative_path_and_reads_file(mocker):
    from introduction.playground.ssrf.main import ssrf_lab

    m = mocker.mock_open(read_data='hello')
    mocker.patch.object(builtins, 'open', m)

    resp = ssrf_lab('blog.txt')

    assert resp == {"blog": "hello"}
    m.assert_called_once()
