"""Delta unit test for XXE hardening.

This patch replaces a custom xml.sax-based parser configuration with defusedxml and adds input validation
(returning 400 on invalid XML).

Assumptions:
- pytest is used.
- We can unit-test the view function as a plain callable by passing a stub request.
- We mock the Django HttpResponseBadRequest factory and logging.
"""

import pytest

from introduction import views


class _Req:
    def __init__(self, body: bytes):
        self.body = body


def test_xxe_parse_invalid_xml_returns_400(monkeypatch):
    # Force defusedxml.parseString to raise, simulating invalid/malicious XML.
    def _raise(_xml):
        raise Exception("bad xml")

    monkeypatch.setattr(views, "parseString", _raise)

    # Capture that we return a bad request response.
    class _BadResp:
        def __init__(self, msg):
            self.status_code = 400
            self.content = msg.encode("utf-8")

    monkeypatch.setattr(views, "HttpResponseBadRequest", lambda msg: _BadResp(msg))

    # Avoid touching templates / Django rendering.
    monkeypatch.setattr(views, "render", lambda request, tpl: "rendered")

    resp = views.xxe_parse(_Req(b"<not-xml"))

    assert getattr(resp, "status_code", None) == 400
    assert b"Invalid XML input" in resp.content
