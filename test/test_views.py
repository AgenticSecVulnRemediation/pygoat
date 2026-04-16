import types

import pytest


@pytest.mark.django_db
def test_a9_lab_uses_safe_load(mocker):
    """Delta behavior: yaml.safe_load is used instead of yaml.load.

    We assert the view invokes yaml.safe_load when parsing uploaded YAML.
    """

    from introduction import views

    safe_load_spy = mocker.patch.object(views.yaml, 'safe_load', autospec=True, return_value={'ok': True})

    class DummyFile:
        pass

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method='POST',
        FILES={'file': DummyFile()},
    )

    response = views.a9_lab(request)

    assert response.status_code == 200
    safe_load_spy.assert_called_once()
