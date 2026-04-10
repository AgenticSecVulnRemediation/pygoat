import io
import logging

import pytest
import yaml


def test_a9_lab_logs_yaml_parse_error(monkeypatch, caplog):
    # Regression test: YAML parsing errors should be caught as yaml.YAMLError and logged.
    from introduction import views

    def raise_yaml_error(_file):
        raise yaml.YAMLError('bad yaml')

    monkeypatch.setattr(views.yaml, 'safe_load', raise_yaml_error)

    class Req:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'
        FILES = {'file': io.BytesIO(b'not: yaml:')}

    with caplog.at_level(logging.ERROR):
        views.a9_lab(Req())

    assert any('YAML parsing error' in rec.message for rec in caplog.records)
