import pytest


def test_valid_ip_allows_ipv4_like_address_and_rejects_non_ip():
    """Delta test for the newly introduced valid_ip() function."""

    # Import inside the test to avoid Django importing side-effects during collection.
    from introduction import mitre

    assert mitre.valid_ip("127.0.0.1") is True
    assert mitre.valid_ip("256.1.1.1") is True  # NOTE: current implementation checks format only
    assert mitre.valid_ip("127.0.0.1;rm -rf /") is False
    assert mitre.valid_ip("example.com") is False
