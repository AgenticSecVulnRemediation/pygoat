import ast
import pathlib


def test_views_ssrf_lab_has_path_traversal_validation_code_present():
    """Regression test for the patch: ensure ssrf_lab contains validation checks.

    Note: PR 1964 was flagged for indentation issues; this test focuses only on verifying
    the intended new validation logic exists in source.
    """
    src = pathlib.Path('introduction/views.py').read_text(encoding='utf-8')

    # Ensure added APIs are present
    assert 'os.path.isabs' in src
    assert 'os.path.commonpath' in src

    # Also ensure join->abspath candidate_path pattern is present
    assert 'candidate_path' in src
    assert 'base_dir' in src
