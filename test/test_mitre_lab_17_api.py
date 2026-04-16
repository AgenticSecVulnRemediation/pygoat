import importlib.util
import pathlib
from types import SimpleNamespace


def _load_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_mitre_lab_17_api_rejects_invalid_ip_before_subprocess(monkeypatch):
    """Delta: invalid ip returns 400 and should not call command_out."""
    src_path = pathlib.Path("introduction/mitre.py")
    mod = _load_module_from_path("intro_mitre", str(src_path))

    monkeypatch.setattr(
        mod,
        "command_out",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("command_out should not be called")),
    )

    request = SimpleNamespace(method="POST", POST={"ip": "1.2.3.4; rm -rf /"})
    resp = mod.mitre_lab_17_api(request)
    assert getattr(resp, "status_code", None) == 400


def test_mitre_lab_17_api_uses_arg_list(monkeypatch):
    """Delta: command passed as ["nmap", ip]"""
    src_path = pathlib.Path("introduction/mitre.py")
    mod = _load_module_from_path("intro_mitre2", str(src_path))

    seen = {}

    def fake_command_out(cmd):
        seen["cmd"] = cmd
        return (b"STATE SERVICE\n\n80/tcp open http\n", b"")

    monkeypatch.setattr(mod, "command_out", fake_command_out)

    request = SimpleNamespace(method="POST", POST={"ip": "127.0.0.1"})
    resp = mod.mitre_lab_17_api(request)

    assert seen["cmd"] == ["nmap", "127.0.0.1"]
    assert resp.status_code == 200
