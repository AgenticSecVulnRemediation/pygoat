# Assumptions:
# - The project uses pytest.
# - introduction.views.safe_make_parser() exists after the fix.

import pytest

from introduction import views


def test_safe_make_parser_disables_external_general_entities():
    """Regression test: XXE mitigation disables external general entities."""

    parser = views.safe_make_parser()

    # xml.sax returns 0/1 ints, but we assert Falsey
    assert parser.getFeature(views.feature_external_ges) in (False, 0)
