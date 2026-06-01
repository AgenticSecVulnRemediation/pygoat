import os
import importlib


def test_ssrf_lab_rejects_path_traversal_outside_base_dir():
    # Arrange
    mod = importlib.import_module('introduction.playground.ssrf.main')

    # Use an absolute path outside the module directory; join(base_dir, abs) would ignore base_dir
    outside_path = os.path.abspath(os.path.join(os.sep, 'etc', 'passwd'))

    # Act
    result = mod.ssrf_lab(outside_path)

    # Assert
    assert isinstance(result, dict)
    assert result.get('blog') == 'Invalid file path.'
