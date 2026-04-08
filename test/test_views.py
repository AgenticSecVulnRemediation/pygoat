import ast
import os
import types
from pathlib import Path

import pytest


def _extract_function_source(source: str, func_name: str) -> str:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            mod = ast.Module(body=[node], type_ignores=[])
            return ast.unparse(mod) + "\n"
    raise AssertionError(f"{func_name} not found as a top-level function")


def _load_ssrf_lab_function():
    """
    Loads only the ssrf_lab() function from introduction/views.py into an isolated module namespace,
    avoiding heavy imports and side effects from the full module.
    """
    views_path = Path("introduction/views.py")
    source = views_path.read_text(encoding="utf-8")
    func_src = _extract_function_source(source, "ssrf_lab")

    mod = types.ModuleType("ssrf_lab_isolated")
    mod.__file__ = str(views_path)

    # Provide only what ssrf_lab needs.
    mod.os = os

    def _redirect(name):
        return ("redirect", name)

    def _render(request, template, context=None):
        return {"template": template, "context": context or {}}

    mod.redirect = _redirect
    mod.render = _render

    exec(compile(func_src, mod.__file__, "exec"), mod.__dict__)
    return mod.ssrf_lab


@pytest.fixture
def ssrf_lab():
    return _load_ssrf_lab_function()


@pytest.fixture
def fake_request():
    class User:
        is_authenticated = True

    class Req:
        user = User()
        method = "POST"
        POST = {"blog": "blog.txt"}

    return Req()


def test_ssrf_lab_redirects_when_unauthenticated(ssrf_lab, fake_request):
    # Arrange
    fake_request.user.is_authenticated = False

    # Act
    result = ssrf_lab(fake_request)

    # Assert
    assert result == ("redirect", "login")


def test_ssrf_lab_rejects_path_traversal_with_dotdot(mocker, ssrf_lab, fake_request):
    # Arrange
    fake_request.POST["blog"] = "../secrets.txt"
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called"))

    # Act
    result = ssrf_lab(fake_request)

    # Assert
    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"] == {"blog": "Invalid file path"}
    open_spy.assert_not_called()


def test_ssrf_lab_rejects_absolute_path(mocker, ssrf_lab, fake_request):
    # Arrange
    fake_request.POST["blog"] = os.path.abspath("somefile.txt")
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called"))

    # Act
    result = ssrf_lab(fake_request)

    # Assert
    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"] == {"blog": "Invalid file path"}
    open_spy.assert_not_called()


def test_ssrf_lab_denies_when_normalized_path_escapes_base_dir(mocker, ssrf_lab, fake_request):
    # Arrange
    fake_request.POST["blog"] = "safe.txt"
    mocker.patch.object(os.path, "dirname", return_value="/base")
    mocker.patch.object(os.path, "join", return_value="/base/safe.txt")
    mocker.patch.object(os.path, "normpath", return_value="/etc/passwd")
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called"))

    # Act
    result = ssrf_lab(fake_request)

    # Assert
    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"] == {"blog": "Access denied"}
    open_spy.assert_not_called()


def test_ssrf_lab_allows_safe_relative_path_and_opens_normalized_path(mocker, ssrf_lab, fake_request):
    # Arrange
    fake_request.POST["blog"] = "blog.txt"
    mocker.patch.object(os.path, "dirname", return_value="/base")
    mocker.patch.object(os.path, "join", return_value="/base/blog.txt")
    mocker.patch.object(os.path, "normpath", return_value="/base/blog.txt")

    file_handle = mocker.Mock()
    file_handle.read.return_value = "BLOG_CONTENT"
    open_spy = mocker.patch("builtins.open", return_value=file_handle)

    # Act
    result = ssrf_lab(fake_request)

    # Assert
    open_spy.assert_called_once_with("/base/blog.txt", "r")
    file_handle.read.assert_called_once()
    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"] == {"blog": "BLOG_CONTENT"}
