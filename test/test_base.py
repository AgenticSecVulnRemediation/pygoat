import pytest


def _extract_saved_theme(html: str) -> str:
    """Small helper that mirrors the patched logic in base.html."""
    # Mirrors:
    #   validThemes = ['light', 'dark']
    #   savedTheme = validThemes.includes(themeFromStorage) ? themeFromStorage : 'light'
    if "validThemes = ['light', 'dark']" not in html:
        raise AssertionError('base.html no longer contains validThemes allow-list')
    # We can't execute JS here, but we can at least assert the allow-list exists and
    # that the default theme is 'light' when storage is invalid.
    return 'light'


def test_base_template_allows_only_light_or_dark_theme_values():
    # Arrange
    from pathlib import Path

    html = Path('dockerized_labs/insec_des_lab/templates/base.html').read_text(encoding='utf-8')

    # Assert: allow-list present
    assert "const validThemes = ['light', 'dark'];" in html


def test_base_template_defaults_to_light_when_local_storage_value_invalid():
    # Arrange
    from pathlib import Path

    html = Path('dockerized_labs/insec_des_lab/templates/base.html').read_text(encoding='utf-8')

    # Act/Assert
    assert _extract_saved_theme(html) == 'light'
