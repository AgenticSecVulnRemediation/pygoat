import os
import pytest


# Tests focus only on the added realpath containment check in ssrf_lab.


def test_ssrf_lab_blocks_path_traversal(monkeypatch):
    from introduction.playground.ssrf import main

    # Arrange: make realpath resolve outside the base dir
    monkeypatch.setattr(main.os.path, 'dirname', lambda _p: '/base')
    monkeypatch.setattr(main.os.path, 'join', lambda a, b: f"{a}/{b}")

    def fake_realpath(p):
        if p == '/base':
            return '/base'
        return '/etc/passwd'

    monkeypatch.setattr(main.os.path, 'realpath', fake_realpath)

    # If open is called, the fix is not working
    monkeypatch.setattr(main, 'open', lambda *a, **k: (_ for _ in ()).throw(AssertionError('open should not be called')), raising=False)

    # Act
    result = main.ssrf_lab('../etc/passwd')

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_allows_file_within_base_dir(monkeypatch):
    from introduction.playground.ssrf import main

    monkeypatch.setattr(main.os.path, 'dirname', lambda _p: '/base')
    monkeypatch.setattr(main.os.path, 'join', lambda a, b: f"{a}/{b}")

    def fake_realpath(p):
        if p == '/base':
            return '/base'
        return '/base/blog.txt'

    monkeypatch.setattr(main.os.path, 'realpath', fake_realpath)

    class DummyFile:
        def read(self):
            return 'ok'

    monkeypatch.setattr(main, 'open', lambda *a, **k: DummyFile(), raising=False)

    result = main.ssrf_lab('blog.txt')

    assert result == {"blog": "ok"}
