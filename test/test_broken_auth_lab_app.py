import runpy
import types
import sys

import pytest


def test_app_run_debug_is_disabled(monkeypatch):
    """Regression test for security fix: app.run must be invoked with debug=False."""

    # Arrange: stub external flask import so module can be executed without Flask installed.
    class DummyFlaskApp:
        def __init__(self, name):
            self.name = name
            self.secret_key = None
            self._run_calls = []

        def route(self, *args, **kwargs):
            def decorator(fn):
                return fn

            return decorator

        def run(self, **kwargs):
            self._run_calls.append(kwargs)

    flask_stub = types.SimpleNamespace(
        Flask=lambda name: DummyFlaskApp(name),
        render_template=lambda *a, **k: "",
        request=types.SimpleNamespace(form=types.SimpleNamespace(get=lambda *_a, **_k: None), cookies={}),
        redirect=lambda *a, **k: "",
        url_for=lambda *a, **k: "",
        make_response=lambda x: x,
        flash=lambda *a, **k: None,
    )

    # Insert stub into sys.modules so `from flask import ...` succeeds
    monkeypatch.setitem(sys.modules, "flask", flask_stub)

    # Act: execute module as __main__ so the guarded app.run block is executed
    # NOTE: using runpy to ensure __name__ == '__main__'
    result_globals = runpy.run_path("dockerized_labs/broken_auth_lab/app.py", run_name="__main__")

    app = result_globals["app"]
    assert hasattr(app, "_run_calls")
    assert len(app._run_calls) == 1

    # Assert: debug is explicitly False after the fix
    kwargs = app._run_calls[0]
    assert kwargs.get("debug") is False
