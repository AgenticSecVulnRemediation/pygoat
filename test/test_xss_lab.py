import pytest


def test_xss_lab_template_escapes_user_query_string():
    """Delta test: template switched from |safe to |escape."""
    from introduction.views import xss_lab

    class _DummyUser:
        is_authenticated = True

    class _DummyGet:
        def get(self, key, default=None):
            return '<script>alert(1)</script>' if key == 'q' else default

    class _DummyRequest:
        user = _DummyUser()
        GET = _DummyGet()

    # Patch FAANG query to return empty so we hit the "query" branch
    from introduction import views

    views.FAANG.objects.filter = lambda company: []

    resp = xss_lab(_DummyRequest())
    body = resp.content.decode('utf-8')

    assert '<script>' not in body
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in body
