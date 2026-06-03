import types


def test_ssrf_lab2_blocks_non_http_scheme(client, django_user_model):
    """Regression test: only http/https URLs are allowed."""
    user = django_user_model.objects.create_user(username="u2", password="p")
    client.force_login(user)

    resp = client.post("/ssrf/lab2", data={"url": "file:///etc/passwd"})
    assert resp.status_code == 200
    assert b"Invalid URL scheme" in resp.content


def test_ssrf_lab2_blocks_internal_address(monkeypatch, client, django_user_model):
    """Regression test: URLs resolving to loopback/private IP must be blocked."""
    import introduction.views as views

    user = django_user_model.objects.create_user(username="u3", password="p")
    client.force_login(user)

    # Force DNS resolution to loopback
    monkeypatch.setattr(views.socket, "gethostbyname", lambda host: "127.0.0.1")

    resp = client.post("/ssrf/lab2", data={"url": "http://example.com/"})
    assert resp.status_code == 200
    assert b"URL resolves to internal address" in resp.content
