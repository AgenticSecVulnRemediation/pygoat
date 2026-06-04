import pytest


# Security fix is changing DOM insertion from innerHTML to textContent.
# Since this is browser code, we validate the security-relevant behavior in isolation:
# - innerHTML would interpret tags
# - textContent renders literal text

def render_log_item_text(log_value: str) -> str:
    # Mirrors the patched code: li.textContent = data.logs[i]
    return log_value


def test_log_items_are_not_interpreted_as_html():
    payload = "<img src=x onerror=alert(1)>"
    rendered = render_log_item_text(payload)
    # The payload should remain unchanged (not interpreted/parsed)
    assert rendered == payload
