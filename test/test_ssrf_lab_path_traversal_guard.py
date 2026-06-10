import pytest


def test_ssrf_lab_rejects_absolute_path(client, django_user_model):
    user = django_user_model.objects.create_user(username="u1", password="p1")
    client.force_login(user)

    # Absolute path should be rejected by new guard
    with pytest.raises(ValueError):
        client.post("/ssrf/lab", {"blog": "/etc/passwd"})


def test_ssrf_lab_rejects_traversal_sequence(client, django_user_model):
    user = django_user_model.objects.create_user(username="u1", password="p1")
    client.force_login(user)

    with pytest.raises(ValueError):
        client.post("/ssrf/lab", {"blog": "../secrets.txt"})
