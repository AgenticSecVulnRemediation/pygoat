import io
import types
import pytest


# Import the Django view module under test
import introduction.views as views


class _User:
    def __init__(self, authenticated: bool):
        self.is_authenticated = authenticated


class _Request:
    def __init__(self, authenticated: bool, yaml_bytes: bytes):
        self.user = _User(authenticated)
        self.method = "POST"
        self.FILES = {"file": io.BytesIO(yaml_bytes)}


def test_a9_lab_uses_safe_load_instead_of_unsafe_yaml_load(mocker):
    """Regression test for YAML deserialization hardening: yaml.safe_load must be used."""

    # Arrange
    req = _Request(authenticated=True, yaml_bytes=b"a: 1\n")

    # If code ever reverts to yaml.load, fail deterministically
    def _boom_load(*args, **kwargs):
        raise AssertionError("yaml.load must not be called; use yaml.safe_load")

    mocker.patch.object(views.yaml, "load", side_effect=_boom_load)

    safe_load_spy = mocker.patch.object(views.yaml, "safe_load", return_value={"a": 1})

    render_spy = mocker.patch.object(views, "render", return_value="rendered")

    # Act
    result = views.a9_lab(req)

    # Assert
    assert result == "rendered"
    safe_load_spy.assert_called_once()
    render_spy.assert_called_once()
