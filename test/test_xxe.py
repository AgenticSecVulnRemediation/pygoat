import pytest


# Assumptions:
# - Django app module path is `introduction.views`.
# - We unit-test only the XXE hardening: external general entities disabled.


def _make_request(authenticated=True, body=b"<root/>"):
    class _User:
        is_authenticated = authenticated

    class _Request:
        user = _User()
        body = body

    return _Request()


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    from introduction import views

    request = _make_request(body=b"<text>hello</text>")

    # Capture the value passed to parser.setFeature(feature_external_ges, ...)
    captured = {}

    class FakeParser:
        def setFeature(self, feature, value):
            captured["feature"] = feature
            captured["value"] = value

    monkeypatch.setattr(views, "make_parser", lambda: FakeParser())

    # Avoid executing real XML parsing; we only care about the security-relevant feature flag.
    monkeypatch.setattr(views, "parseString", lambda *_args, **_kwargs: [])

    # Avoid DB update and template rendering.
    class _Comments:
        class objects:
            @staticmethod
            def filter(**_kwargs):
                class _Q:
                    @staticmethod
                    def update(**_kwargs2):
                        return 1

                return _Q()

    monkeypatch.setattr(views, "comments", _Comments)
    monkeypatch.setattr(views, "render", lambda *_args, **_kwargs: "ok")

    views.xxe_parse(request)

    assert captured["value"] is False
