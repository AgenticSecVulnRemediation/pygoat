# Assumptions:
# - Project uses pytest.
# - The Django views module is importable as "introduction.views".
# - We avoid importing/starting Django; we only validate the security-relevant parser selection.

import importlib


def test_views_imports_defusedxml_make_parser_for_xxe_mitigation():
    """Regression test for XXE hardening: ensure xml.sax.make_parser is not used.

    The patch switches to defusedxml.sax.make_parser. This test asserts the module
    actually binds make_parser from defusedxml, preventing a regression.
    """
    views = importlib.import_module("introduction.views")

    # The function should originate from defusedxml.sax, not xml.sax.
    assert views.make_parser.__module__ == "defusedxml.sax"
