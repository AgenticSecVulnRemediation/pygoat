import ast
import types
from pathlib import Path


def _extract_top_level_nodes(source: str, names: set[str]) -> str:
    """
    Extracts top-level assignments/if blocks that define the requested names.
    This avoids executing unrelated imports (e.g., Django) in settings.py.
    """
    tree = ast.parse(source)
    selected = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    selected.append(node)
                    break
        elif isinstance(node, ast.If):
            # Include the if-block if it assigns any requested names in either branch
            def assigns_requested(stmts):
                for st in stmts:
                    if isinstance(st, ast.Assign):
                        for t in st.targets:
                            if isinstance(t, ast.Name) and t.id in names:
                                return True
                return False

            if assigns_requested(node.body) or assigns_requested(node.orelse):
                selected.append(node)

    mod = ast.Module(body=selected, type_ignores=[])
    return ast.unparse(mod) + "\n"


def _exec_settings_snippet(source: str, module_name: str):
    module = types.ModuleType(module_name)
    module.__file__ = module_name + ".py"
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


def test_settings_sets_secure_cookies_false_when_debug_true():
    # Arrange
    settings_path = Path("dockerized_labs/sensitive_data_exposure/sensitive_data_lab/settings.py")
    full_source = settings_path.read_text(encoding="utf-8")
    snippet = _extract_top_level_nodes(
        full_source,
        {"DEBUG", "SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE"},
    )

    # Act
    settings = _exec_settings_snippet(snippet, module_name="settings_snippet_debug_true")

    # Assert
    assert settings.DEBUG is True
    assert settings.SESSION_COOKIE_SECURE is False
    assert settings.CSRF_COOKIE_SECURE is False


def test_settings_sets_secure_cookies_true_when_debug_false():
    # Arrange
    settings_path = Path("dockerized_labs/sensitive_data_exposure/sensitive_data_lab/settings.py")
    full_source = settings_path.read_text(encoding="utf-8")
    snippet = _extract_top_level_nodes(
        full_source,
        {"DEBUG", "SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE"},
    ).replace("DEBUG = True", "DEBUG = False", 1)

    # Act
    settings = _exec_settings_snippet(snippet, module_name="settings_snippet_debug_false")

    # Assert
    assert settings.DEBUG is False
    assert settings.SESSION_COOKIE_SECURE is True
    assert settings.CSRF_COOKIE_SECURE is True
