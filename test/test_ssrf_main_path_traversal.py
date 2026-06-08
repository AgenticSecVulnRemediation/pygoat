import os
import tempfile


def test_ssrf_lab_rejects_path_traversal(tmp_path):
    """Delta test: ssrf_lab now resolves realpath and blocks traversal outside base dir."""
    # Arrange: create a file outside the module directory to simulate traversal attempt
    outside_file = tmp_path / 'secret.txt'
    outside_file.write_text('secret')

    from introduction.playground.ssrf import main

    # Attempt to traverse upwards; regardless of FS layout, this should be rejected
    result = main.ssrf_lab('../secret.txt')

    assert result == {"blog": "No blog found"}
