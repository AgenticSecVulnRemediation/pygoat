import pytest


# Delta covered: xxe_parse now disables external entities via feature_external_ges=False.

def test_xxe_parse_disables_external_entities(mocker):
    from introduction import views

    # Provide a fake parser that records setFeature calls.
    parser = mocker.Mock()
    mocker.patch.object(views, "make_parser", return_value=parser)

    # Avoid real pulldom parsing and DB update.
    def fake_parse_string(_xml, parser=None):
        assert parser is parser  # ensure parser is passed
        return []

    mocker.patch.object(views, "parseString", side_effect=fake_parse_string)
    mocker.patch.object(views.comments, "objects", mocker.Mock(filter=mocker.Mock(return_value=mocker.Mock(update=mocker.Mock(return_value=1)))))
    mocker.patch.object(views, "render", return_value="OK")

    class DummyRequest:
        def __init__(self):
            self.body = b"<root><text>hi</text></root>"
            self.user = mocker.Mock(is_authenticated=True)

    views.xxe_parse(DummyRequest())

    parser.setFeature.assert_called_with(views.feature_external_ges, False)
