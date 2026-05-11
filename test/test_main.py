import os


def test_ssrf_lab_rejects_invalid_file_paths(monkeypatch):
    """Delta: ssrf_lab now rejects absolute paths and parent traversal."""
    from introduction.playground.ssrf import main

    def _fake_open(*_args, **_kwargs):
        raise AssertionError("open() must not be called for invalid file paths")

    monkeypatch.setattr(main, "open", _fake_open)

    assert main.ssrf_lab(os.path.abspath('x.txt')) == {"blog": "No blog found"}
    assert main.ssrf_lab("../x.txt") == {"blog": "No blog found"}
