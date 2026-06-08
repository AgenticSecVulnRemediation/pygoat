import pytest


def test_views_ssrf_lab2_has_host_allowlist_check():
    """Delta test: ensure SSRF lab2 validates hostname against an allowlist before requests.get."""

    with open("introduction/views.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "from urllib.parse import urlparse" in content
    assert "allowed_hosts" in content
    assert "parsed_url = urlparse(url)" in content
    assert "if parsed_url.hostname not in allowed_hosts" in content
