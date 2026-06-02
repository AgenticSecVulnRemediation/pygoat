import builtins

import pytest


def test_playground_ssrf_lab_blocks_directory_escape(mocker, tmp_path):
    # Import the fixed function
    from introduction.playground.ssrf.main import ssrf_lab

    # Arrange: even if such a file exists elsewhere, traversal must be blocked.
    outside = tmp_path / "outside.txt"
    outside.write_text("secret")

    # Create a fake base_dir and force os.path.abspath/dirname behavior by patching
    # os.path.abspath/join/dirname in module under test would be brittle; instead patch open.
    open_spy = mocker.patch.object(builtins, "open", autospec=True)

    # Act
    result = ssrf_lab("../outside.txt")

    # Assert: function catches ValueError and returns 'No blog found' without opening.
    assert result == {"blog": "No blog found"}
    open_spy.assert_not_called()
