import os


def test_ssrf_lab_rejects_path_traversal_and_does_not_open_file(mocker):
    """Delta: resolved path must stay under base directory; traversal is blocked."""
    from introduction.playground.ssrf.main import ssrf_lab

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))

    result = ssrf_lab("../secrets.txt")

    assert result == {"blog": "No blog found"}
    open_mock.assert_not_called()


def test_ssrf_lab_opens_resolved_path_when_under_base_dir(mocker, tmp_path):
    """Delta: safe paths under base_dir are opened via the resolved real path."""
    import introduction.playground.ssrf.main as main

    fake_dir = tmp_path / "mod"
    fake_dir.mkdir()
    (fake_dir / "blog.txt").write_text("hello")

    mocker.patch.object(main, "__file__", str(fake_dir / "main.py"))

    open_spy = mocker.spy(main, "open")

    result = main.ssrf_lab("blog.txt")

    assert result == {"blog": "hello"}
    assert open_spy.call_count == 1
    opened_path = open_spy.call_args[0][0]
    assert os.path.realpath(opened_path) == os.path.realpath(str(fake_dir / "blog.txt"))
