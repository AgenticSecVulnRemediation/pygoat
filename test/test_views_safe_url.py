import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import introduction.views as views  # noqa: E402


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com/",  # wrong scheme
        "https://evil.com/",  # wrong host
        "file:///etc/passwd",  # dangerous scheme
    ],
)
def test_safe_url_disallows_non_https_or_unapproved_domains(url):
    assert views.safe_url(url) is None


def test_safe_url_allows_https_on_allowed_domain():
    assert views.safe_url("https://example.com/path") == "https://example.com/path"
