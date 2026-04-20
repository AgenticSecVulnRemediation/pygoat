import pathlib

import pytest


def test_a9_js_uses_textcontent_instead_of_innerhtml_for_logs():
    js_path = pathlib.Path("introduction/static/js/a9.js")
    if not js_path.exists():
        pytest.skip("a9.js not present in test environment")

    src = js_path.read_text(encoding="utf-8")

    assert "li.textContent = data.logs[i]" in src
    assert "li.innerHTML = data.logs[i]" not in src
