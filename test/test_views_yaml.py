# Assumptions:
# - This repo uses pytest and pytest-mock.
# - We patch out yaml.safe_load to avoid depending on PyYAML loader behavior.


def test_a9_lab_uses_yaml_safe_load_instead_of_yaml_load(mocker):
    """Delta: a9_lab should call yaml.safe_load (not yaml.load with Loader)."""
    from introduction import views

    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.FILES = {"file": object()}

    safe_load = mocker.patch.object(views.yaml, "safe_load", return_value={"k": "v"})
    # If old vulnerable path is used, fail fast
    mocker.patch.object(views.yaml, "load", side_effect=AssertionError("yaml.load must not be used"))

    # Avoid template rendering dependency: just pass-through a sentinel response
    sentinel = object()

    def _render(_request, _template, context=None):
        # Ensure returned data is the safe_load result
        assert context["data"] == {"k": "v"}
        return sentinel

    mocker.patch.object(views, "render", side_effect=_render)

    # Act
    resp = views.a9_lab(request)

    # Assert
    assert resp is sentinel
    safe_load.assert_called_once_with(request.FILES["file"])
