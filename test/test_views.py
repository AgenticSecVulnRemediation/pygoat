import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _import_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_ssrf_lab_rejects_path_traversal_with_parent_dir_segment(mocker):
    views_path = Path(__file__).resolve().parents[1] / "introduction" / "views.py"
    views = _import_module_from_path("introduction_views_under_test", views_path)

    render_mock = mocker.patch.object(views, "render", autospec=True, return_value=object())
    open_mock = mocker.patch("builtins.open", autospec=True)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": "../secrets.txt"},
    )

    result = views.ssrf_lab(request)

    assert result is render_mock.return_value
    render_mock.assert_called_once()
    assert render_mock.call_args.args[1] == "Lab/ssrf/ssrf_lab.html"
    assert render_mock.call_args.args[2] == {"blog": "Invalid file path"}
    open_mock.assert_not_called()


def test_ssrf_lab_rejects_absolute_path(mocker):
    views_path = Path(__file__).resolve().parents[1] / "introduction" / "views.py"
    views = _import_module_from_path("introduction_views_under_test_abs", views_path)

    render_mock = mocker.patch.object(views, "render", autospec=True, return_value=object())
    open_mock = mocker.patch("builtins.open", autospec=True)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": "/etc/passwd"},
    )

    result = views.ssrf_lab(request)

    assert result is render_mock.return_value
    assert render_mock.call_args.args[2] == {"blog": "Invalid file path"}
    open_mock.assert_not_called()


def test_ssrf_lab_denies_when_normalized_path_escapes_base_dir(mocker):
    views_path = Path(__file__).resolve().parents[1] / "introduction" / "views.py"
    views = _import_module_from_path("introduction_views_under_test_norm", views_path)

    # Validate the second guard: deny access when the normalized path is outside the base directory.
    mocker.patch.object(views.os.path, "dirname", autospec=True, return_value="/base")
    mocker.patch.object(views.os.path, "isabs", autospec=True, return_value=False)
    mocker.patch.object(views.os.path, "join", autospec=True, return_value="/base/child")
    mocker.patch.object(views.os.path, "normpath", autospec=True, return_value="/escaped/child")

    render_mock = mocker.patch.object(views, "render", autospec=True, return_value=object())
    open_mock = mocker.patch("builtins.open", autospec=True)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": "child"},
    )

    result = views.ssrf_lab(request)

    assert result is render_mock.return_value
    render_mock.assert_called_once()
    assert render_mock.call_args.args[2] == {"blog": "Access denied"}
    open_mock.assert_not_called()
