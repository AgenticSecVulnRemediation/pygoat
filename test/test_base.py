# Assumption: base template is not executed in tests; we validate the patched allowlist behavior by
# executing the embedded script via jsdom.

import re

import pytest

jsdom = pytest.importorskip("jsdom")


def _extract_script(html: str) -> str:
    # Extract first <script>...</script> block.
    m = re.search(r"<script>([\s\S]*?)</script>", html)
    assert m, "No <script> block found"
    return m.group(1)


def test_theme_on_load_uses_allowlist_and_defaults_to_light_for_unexpected_values(tmp_path):
    from dockerized_labs.insec_des_lab.templates import base as _  # noqa: F401

    # Read the actual template file content
    html = (tmp_path.cwd() / "dockerized_labs/insec_des_lab/templates/base.html").read_text(encoding="utf-8")
    script = _extract_script(html)

    from jsdom import JSDOM  # type: ignore

    dom = JSDOM(
        "<html data-theme='light'><body><button class='theme-toggle'></button></body></html>",
        runScripts="dangerously",
        url="http://localhost",
    )

    # Set an attacker-controlled unexpected value
    dom.window.localStorage.setItem("theme", "<img src=x onerror=alert(1)>")

    dom.window.eval(script)

    # Fire DOMContentLoaded to trigger patched code
    dom.window.document.dispatchEvent(dom.window.Event("DOMContentLoaded"))

    assert dom.window.document.documentElement.getAttribute("data-theme") == "light"
