import os

import pytest


def test_ssrf_lab_rejects_path_traversal_and_does_not_open_file(mocker):
    """Delta: resolved path must stay under base directory; traversal returns 'No blog found'."""
    from introduction.playground.ssrf.main import ssrf_lab

    # Ensure open is not used when traversal is detected
    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))

    # '../' should resolve outside base directory
    result = ssrf_lab("../secrets.txt")

    assert result == {"blog": "No blog found"}
    open_mock.assert_not_called()


def test_ssrf_lab_opens_real_path_when_under_base_dir(mocker, tmp_path):
    """Delta: when file resolves under base_dir, open is called with the real_path."""
    # Import module to patch __file__ base dir logic
    import introduction.playground.ssrf.main as main

    # Arrange fake module location
    fake_dir = tmp_path / "mod"
    fake_dir.mkdir()
    (fake_dir / "blog.txt").write_text("hello")

    mocker.patch.object(main, "__file__", str(fake_dir / "main.py"))

    open_spy = mocker.spy(main, "open")  # builtins.open as seen by module

    # Act
    result = main.ssrf_lab("blog.txt")

    # Assert
    assert result == {"blog": "hello"}
    assert open_spy.call_count == 1
    opened_path = open_spy.call_args[0][0]
    assert os.path.realpath(opened_path) == os.path.realpath(str(fake_dir / "blog.txt"))
