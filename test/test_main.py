import pytest


# Assumption: module path maps to repo structure and is importable as a package.
# If the project uses a different import layout, adjust the import accordingly.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    with pytest.raises(ValueError, match="potential path traversal"):
        ssrf_lab("/etc/passwd")


@pytest.mark.parametrize("path", [
    "../secret.txt",
    "..\\secret.txt",
    "blog/../../secret.txt",
])
def test_ssrf_lab_rejects_parent_traversal(path):
    with pytest.raises(ValueError, match="potential path traversal"):
        ssrf_lab(path)
