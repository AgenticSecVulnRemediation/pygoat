import os
import tempfile

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_outside_base_directory(monkeypatch):
    # Arrange: create a tmp directory for the module directory and a file outside it
    with tempfile.TemporaryDirectory() as base_dir:
        with tempfile.TemporaryDirectory() as outside_dir:
            outside_file = os.path.join(outside_dir, "secret.txt")
            with open(outside_file, "w", encoding="utf-8") as f:
                f.write("SECRET")

            # Make ssrf_lab's __file__ appear to be inside base_dir
            fake_file = os.path.join(base_dir, "main.py")

            import introduction.playground.ssrf.main as mod

            monkeypatch.setattr(mod, "__file__", fake_file)

            # Act: attempt traversal to outside_dir
            rel = os.path.relpath(outside_file, base_dir)
            traversal = os.path.join("..", rel) if not rel.startswith("..") else rel

            res = ssrf_lab(traversal)

            # Assert
            assert res == {"blog": "No blog found"}


def test_ssrf_lab_allows_reading_file_within_base_directory(monkeypatch):
    with tempfile.TemporaryDirectory() as base_dir:
        inside_file = os.path.join(base_dir, "blog.txt")
        with open(inside_file, "w", encoding="utf-8") as f:
            f.write("HELLO")

        fake_file = os.path.join(base_dir, "main.py")

        import introduction.playground.ssrf.main as mod

        monkeypatch.setattr(mod, "__file__", fake_file)

        res = ssrf_lab("blog.txt")
        assert res == {"blog": "HELLO"}
