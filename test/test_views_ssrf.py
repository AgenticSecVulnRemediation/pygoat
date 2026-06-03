def test_ssrf_lab_rejects_traversal_path_returns_invalid_file_path_message(client, django_user_model):
    """Regression test for path traversal in SSRF lab view.

    The view should detect '..' and/or absolute paths and not attempt to open.
    """
    # This project uses Django; assume test client fixture is available.
    # If not, this test will be adapted by the repo's existing pytest-django setup.

    # Arrange: login user
    user = django_user_model.objects.create_user(username="u", password="p")
    client.force_login(user)

    # Act
    resp = client.post("/ssrf/lab", data={"blog": "../etc/passwd"})

    # Assert: response contains the fixed error message
    assert resp.status_code == 200
    assert b"Invalid file path provided" in resp.content
