import builtins

import pytest


def test_yaml_uses_safe_load(monkeypatch):
    """Regression test: ensure yaml.load is not used (prevents unsafe object construction)."""
    # Arrange
    import importlib

    # Patch yaml.load to raise if called; safe_load should still be called.
    import yaml

    def _boom(*args, **kwargs):
        raise AssertionError('yaml.load should not be called')

    monkeypatch.setattr(yaml, 'load', _boom)

    safe_load_called = {'called': False}
    real_safe_load = yaml.safe_load

    def _safe_load_wrapper(*args, **kwargs):
        safe_load_called['called'] = True
        return real_safe_load(*args, **kwargs)

    monkeypatch.setattr(yaml, 'safe_load', _safe_load_wrapper)

    # Patch open used by the module to provide a YAML string
    class _FakeFile:
        def __init__(self, s):
            self._s = s

        def read(self):
            return self._s

        def __iter__(self):
            return iter(self._s.splitlines(True))

        def close(self):
            pass

    monkeypatch.setattr(builtins, 'open', lambda *a, **k: _FakeFile('a: 1\n'))

    # Act: import/reload module so top-level code executes
    mod = importlib.import_module('introduction.lab_code.test')
    importlib.reload(mod)

    # Assert
    assert safe_load_called['called'] is True
