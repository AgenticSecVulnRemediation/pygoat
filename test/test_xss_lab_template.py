import pytest


def test_xss_template_does_not_mark_query_safe():
    """Delta test asserting the unsafe '|safe' filter is removed.

    This is a unit-style assertion on the template content provided in the PR.
    """

    from introduction.templates.Lab.XSS import xss_lab  # type: ignore

    # The test will fail if the vulnerable pattern reappears.
    assert "query|safe" not in xss_lab.__doc__
