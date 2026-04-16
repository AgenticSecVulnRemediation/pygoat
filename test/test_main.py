import os
import importlib.util
import pathlib


def _load_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_ssrf_lab_blocks_directory_traversal_outside_module_dir():
    # Assumption: project root is current working directory when running tests.
    src_path = pathlib.Path("introduction/playground/ssrf/main.py")
    mod = _load_module_from_path("ssrf_main", str(src_path))

    # Attempt to read outside the module directory; should be blocked and return safe default.
    res = mod.ssrf_lab("../secrets.txt")
    assert res == {"blog": "No blog found"}

    # Attempt with absolute path should also be blocked.
    res2 = mod.ssrf_lab(os.path.abspath("/etc/passwd"))
    assert res2 == {"blog": "No blog found"}
