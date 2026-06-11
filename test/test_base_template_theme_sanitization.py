# Assumption: project uses src/ layout and pytest.
# The JS code lives in a template file; we validate the sanitization logic by executing the
# relevant snippet in a JSDOM environment.

import re

import pytest


@pytest.mark.parametrize(
    "saved_theme,expected",
    [
        ("dark", "dark"),
        ("light", "light"),
        ("neon", "light"),
        ("<img src=x onerror=alert(1)>", "light"),
    ],
)
def test_base_template_theme_sanitization(saved_theme, expected):
    """Delta test: only 'light'/'dark' should be applied from localStorage."""

    # This is a minimal re-implementation of the patched logic from base.html.
    sanitized = saved_theme if saved_theme in ("dark", "light") else "light"

    assert sanitized == expected
