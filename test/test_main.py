import os


def test_ssrf_lab_blocks_path_traversal(tmp_path, monkeypatch):
    """Delta test: ssrf_lab now rejects '..' and absolute paths and constrains to base dir."""

    # Arrange: create a fake module directory
    module_dir = tmp_path / "mod"
    module_dir.mkdir()
    blog = module_dir / "blog.txt"
    blog.write_text("hello")

    import introduction.playground.ssrf.main as ssrf_main

    # Monkeypatch __file__ to be inside module_dir
    monkeypatch.setattr(ssrf_main, "__file__", str(module_dir / "main.py"))

    # Act + Assert: traversal
    assert ssrf_main.ssrf_lab("../secret.txt") == {"blog": "No blog found"}

    # Act + Assert: absolute path
    assert ssrf_main.ssrf_lab(str(blog.resolve())) == {"blog": "No blog found"}

    # Act + Assert: valid relative path works
    assert ssrf_main.ssrf_lab("blog.txt") == {"blog": "hello"}
