import importlib.util
from pathlib import Path


def _import_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _exec_settings_with_debug_overridden(settings_path: Path, debug_value: bool):
    """Execute settings.py in an isolated module namespace with DEBUG overridden.

    This avoids relying on Django settings machinery and allows testing both branches
    of the DEBUG conditional added by the security fix.
    """
    source = settings_path.read_text(encoding="utf-8")

    # Replace the first occurrence of "DEBUG = ..." with the desired value.
    # This is intentionally narrow to target the exact assignment in the file.
    needle = "DEBUG = True"
    replacement = f"DEBUG = {str(debug_value)}"
    if needle in source:
        source = source.replace(needle, replacement, 1)
    else:
        # Fallback: handle if DEBUG is set differently but still as a simple assignment.
        import re

        source, n = re.subn(r"^DEBUG\s*=\s*.*$", replacement, source, count=1, flags=re.MULTILINE)
        assert n == 1, "Could not override DEBUG assignment in settings.py"

    module_name = f"sensitive_data_lab_settings_debug_{'false' if not debug_value else 'true'}"
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(settings_path)
    exec(compile(source, str(settings_path), "exec"), module.__dict__)
    return module


def test_settings_secure_cookie_flags_follow_debug_flag_debug_true_branch():
    settings_path = (
        Path(__file__).resolve().parents[1]
        / "dockerized_labs"
        / "sensitive_data_exposure"
        / "sensitive_data_lab"
        / "settings.py"
    )

    settings = _import_module_from_path("sensitive_data_lab_settings_under_test", settings_path)

    # Delta behavior: when DEBUG is True, secure flags must be explicitly False.
    assert settings.DEBUG is True
    assert settings.SESSION_COOKIE_SECURE is False
    assert settings.CSRF_COOKIE_SECURE is False


def test_settings_secure_cookie_flags_follow_debug_flag_debug_false_branch():
    settings_path = (
        Path(__file__).resolve().parents[1]
        / "dockerized_labs"
        / "sensitive_data_exposure"
        / "sensitive_data_lab"
        / "settings.py"
    )

    settings = _exec_settings_with_debug_overridden(settings_path, debug_value=False)

    # Security fix: in production (DEBUG=False), secure cookie flags must be enabled.
    assert settings.DEBUG is False
    assert settings.SESSION_COOKIE_SECURE is True
    assert settings.CSRF_COOKIE_SECURE is True
