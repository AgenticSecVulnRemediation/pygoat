import os

import pytest


class _Req:
    def __init__(self, blog_value: str):
        self.user = type("U", (), {"is_authenticated": True})()
        self.method = "POST"
        self.POST = {"blog": blog_value}


@pytest.mark.parametrize(
    "blog_value",
    [
        "/etc/passwd",
        "../secrets.txt",
        "..\\secrets.txt",
    ],
)
def test_ssrf_lab_rejects_absolute_or_traversal_paths(blog_value):
    """Regression test for SSRF/path traversal mitigation.

    Patch added a guard:
      if os.path.isabs(file) or '..' in file: raise ValueError
    """

    from introduction import views

    with pytest.raises(ValueError, match="Invalid file path provided"):
        views.ssrf_lab(_Req(blog_value))
