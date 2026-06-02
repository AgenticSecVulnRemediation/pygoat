# Assumptions:
# - Django is available in the test environment.
# - The project uses pytest + pytest-django.
# - The 'introduction' Django app is importable.

import pytest
from django.test import RequestFactory


@pytest.mark.django_db
def test_ssrf_lab_rejects_directory_traversal_paths():
    """Regression test for path traversal prevention in ssrf_lab.

    The fix adds validation for '..' and absolute paths and ensures resolved path stays under the app dir.
    """
    from introduction import views

    rf = RequestFactory()
    req = rf.post("/ssrf/lab", data={"blog": "../secrets.txt"})

    # Satisfy authentication check used throughout views.
    class _User:
        is_authenticated = True

    req.user = _User()

    resp = views.ssrf_lab(req)
    assert resp.status_code == 200
    # Should not attempt to read file; should show invalid file path message
    assert b"Invalid file path" in resp.content


@pytest.mark.django_db
def test_ssrf_lab_rejects_absolute_paths(tmp_path):
    from introduction import views

    rf = RequestFactory()
    req = rf.post("/ssrf/lab", data={"blog": "/etc/passwd"})

    class _User:
        is_authenticated = True

    req.user = _User()

    resp = views.ssrf_lab(req)
    assert resp.status_code == 200
    assert b"Invalid file path" in resp.content
