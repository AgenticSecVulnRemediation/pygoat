import os
import pytest


def test_ssrf_lab_file_read_blocks_path_traversal(monkeypatch, tmp_path):
    """Delta test for ssrf_lab in views.py: it should reject paths that escape the base directory."""
    import introduction.views as views

    # Create a fake base directory and a file outside of it
    base_dir = tmp_path / 'base'
    base_dir.mkdir()
    outside = tmp_path / 'outside.txt'
    outside.write_text('secret')

    # Monkeypatch __file__ dirname resolution by patching os.path.dirname within the module
    monkeypatch.setattr(views.os.path, 'dirname', lambda _: str(base_dir))

    # Payload attempts to escape base_dir
    file_param = '../outside.txt'

    # Act: mimic the critical portion of code by calling ssrf_lab view via a dummy request
    from django.test import RequestFactory
    rf = RequestFactory()
    request = rf.post('/ssrf', data={'blog': file_param})

    # Need an authenticated user per the view; set a simple object with is_authenticated=True
    class U:
        is_authenticated = True

    request.user = U()

    response = views.ssrf_lab(request)

    # Assert: should fall into except and show no blog found
    assert response.status_code == 200
    assert 'No blog found' in response.content.decode('utf-8')
