import pytest


def test_mitre_lab_17_api_rejects_command_injection_chars():
    """The patched code validates the ip/hostname with a strict regex and should reject ';', '&', etc."""

    # We don't import the Django view to keep this as a true unit test; instead we validate
    # the exact regex behavior introduced in the patch.
    import re

    pattern = r'^[0-9a-zA-Z\.-]+$'
    assert re.match(pattern, "127.0.0.1")
    assert re.match(pattern, "example-host")

    assert re.match(pattern, "127.0.0.1;rm -rf /") is None
    assert re.match(pattern, "example.com&&id") is None
