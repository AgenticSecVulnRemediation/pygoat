import pytest


# Assumption: module path is importable from repo root.
import introduction.views as views


def test_a9_lab_uses_safe_load_instead_of_yaml_load(mocker):
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"

    # file is required by the view; contents don't matter because we'll intercept YAML loading
    request.FILES = {"file": mocker.Mock()}

    safe_load_spy = mocker.spy(views.yaml, "safe_load")
    load_spy = mocker.spy(views.yaml, "load")

    # Act
    views.a9_lab(request)

    # Assert
    assert safe_load_spy.called
    assert not load_spy.called
