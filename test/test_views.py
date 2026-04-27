import os
import pytest

from introduction import views


def test_ssrf_lab_blocks_path_traversal_via_realpath_containment(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = 'POST'
    request.POST = {'blog': '../outside.txt'}

    base_dir = '/app/introduction'
    mocker.patch.object(views.os.path, 'realpath', side_effect=[base_dir, '/etc/passwd'])
    mocker.patch.object(views.os.path, 'dirname', return_value='/app/introduction')
    mocker.patch.object(views.os, 'sep', os.sep)

    render_mock = mocker.patch.object(views, 'render', return_value='rendered')

    # Act
    resp = views.ssrf_lab(request)

    # Assert: should hit the except and return "No blog found" rendering (and not open any file)
    assert resp == 'rendered'
    render_mock.assert_called()
    args, kwargs = render_mock.call_args
    assert kwargs.get('context', args[2] if len(args) > 2 else {})['blog'] == 'No blog found'
