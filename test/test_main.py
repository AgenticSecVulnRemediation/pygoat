import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_outside_allowed_dir(tmp_path, monkeypatch):
    """Regression: ensure path traversal can't escape allowed_dir."""
    # Arrange: pretend the module lives in tmp_path / 'pkg'
    fake_module_dir = tmp_path / 'pkg'
    fake_module_dir.mkdir()
    (fake_module_dir / 'safe.txt').write_text('SAFE', encoding='utf-8')
    (tmp_path / 'secret.txt').write_text('SECRET', encoding='utf-8')

    import introduction.playground.ssrf.main as ssrf_main
    monkeypatch.setattr(ssrf_main, '__file__', str(fake_module_dir / 'main.py'))

    # Act
    result = ssrf_lab('../secret.txt')

    # Assert
    assert result == {"blog": "Invalid file path"}


def test_ssrf_lab_allows_read_within_allowed_dir(tmp_path, monkeypatch):
    # Arrange
    fake_module_dir = tmp_path / 'pkg'
    fake_module_dir.mkdir()
    (fake_module_dir / 'safe.txt').write_text('SAFE', encoding='utf-8')

    import introduction.playground.ssrf.main as ssrf_main
    monkeypatch.setattr(ssrf_main, '__file__', str(fake_module_dir / 'main.py'))

    # Act
    result = ssrf_lab('safe.txt')

    # Assert
    assert result == {"blog": "SAFE"}
