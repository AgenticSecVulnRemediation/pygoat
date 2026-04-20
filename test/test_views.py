import pytest


def test_defusedxml_sax_make_parser_disables_external_entities_by_default():
    """Delta test: views.py now imports make_parser from defusedxml.sax.

    We verify the parser produced does not allow enabling external general entities.
    In the stdlib xml.sax parser, feature_external_ges can commonly be set True.
    DefusedXML's hardened parser should prevent that.
    """

    defusedxml = pytest.importorskip("defusedxml")
    from defusedxml.sax import make_parser
    from xml.sax.handler import feature_external_ges

    parser = make_parser()

    with pytest.raises(Exception):
        parser.setFeature(feature_external_ges, True)
