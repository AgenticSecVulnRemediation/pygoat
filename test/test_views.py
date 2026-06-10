import pytest

import introduction.views as views


def test_make_parser_imports_from_defusedxml_sax(mocker):
    """Delta test: ensure views.make_parser refers to defusedxml.sax.make_parser (not xml.sax)."""

    # Arrange
    defused_make_parser = mocker.Mock(name="defused_make_parser")

    # Replace views.make_parser; if code changes back to xml.sax, this test will break because
    # module-level reference would be different.
    views.make_parser = defused_make_parser

    # Act
    parser = views.make_parser()

    # Assert
    defused_make_parser.assert_called_once_with()
    assert parser is defused_make_parser.return_value
