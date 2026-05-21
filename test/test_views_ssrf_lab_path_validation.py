import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import introduction.views as views  # noqa: E402


def test_ssrf_lab_rejects_directory_traversal_file_path(mocker):
    """Regression test: ssrf_lab must reject .. and absolute paths before opening file."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST.__getitem__.side_effect = lambda k: {"blog": "../secrets.txt"}[k]

    open_spy = mocker.patch("builtins.open", autospec=True)

    # Act
    response = views.ssrf_lab(request)

    # Assert
    open_spy.assert_not_called()
    # response is a Django HttpResponse from render(); verify context payload via template_name? not available here,
    # so assert type and that it contains our message.
    assert hasattr(response, "content")
    assert b"Invalid file path specified" in response.content
