import pytest


# This test asserts that user-provided theme values are validated to known-safe values.
# Since the code is embedded in a template, we validate the exact security-relevant logic in isolation.

def apply_theme(saved_theme: str) -> str:
    # Mirrors the patched logic in dockerized_labs/insec_des_lab/templates/base.html
    if saved_theme != "dark" and saved_theme != "light":
        saved_theme = "light"
    return saved_theme


@pytest.mark.parametrize("value", ["dark", "light"])
def test_apply_theme_allows_only_expected_values(value):
    assert apply_theme(value) == value


@pytest.mark.parametrize("value", [
    "<img src=x onerror=alert(1)>",
    "dark\" onload=alert(1) \"",
    "unknown",
    "",
])
def test_apply_theme_falls_back_to_light_for_unexpected_values(value):
    assert apply_theme(value) == "light"
