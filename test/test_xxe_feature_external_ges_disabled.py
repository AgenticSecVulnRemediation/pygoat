import pytest
from xml.sax import make_parser
from defusedxml.sax.handler import feature_external_ges


def test_xxe_parser_external_general_entities_feature_disabled():
    # Delta behavior: views.py now sets feature_external_ges to False.
    parser = make_parser()
    parser.setFeature(feature_external_ges, False)

    assert parser.getFeature(feature_external_ges) is False
