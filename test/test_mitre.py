from types import SimpleNamespace

import pytest

# Assumption: tests run in repo root where 'introduction' package is importable.
import introduction.mitre as mitre


def _fake_post_request(ip_value):
    return SimpleNamespace(method="POST", POST={"ip": ip_value})


def test_mitre_lab_17_api_invalid_ip_returns_400_and_does_not_execute_command(monkeypatch):
    """Regression for command-injection fix: reject invalid IP before building/executing nmap."""

    def boom(_cmd):
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", boom)

    resp = mitre.mitre_lab_17_api(_fake_post_request("127.0.0.1; rm -rf /"))

    assert getattr(resp, "status_code", None) == 400


def test_mitre_lab_17_api_uses_argv_list_for_nmap(monkeypatch):
    """Regression: ensure subprocess execution is invoked with argv list (no shell)."""
    seen = {}

    def fake_command_out(cmd):
        seen["cmd"] = cmd
        # minimal output that matches the regex parsing in the view
        out = b"STATE SERVICE\n\n22/tcp open ssh\n"
        err = b""
        return out, err

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    resp = mitre.mitre_lab_17_api(_fake_post_request("127.0.0.1"))

    assert seen["cmd"] == ["nmap", "127.0.0.1"]
    assert resp.status_code == 200
    payload = resp.json()
    assert "ports" in payload
    assert payload["ports"] == ["22/tcp open ssh"]
