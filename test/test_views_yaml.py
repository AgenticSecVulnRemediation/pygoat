import importlib


def test_views_uses_safe_load_in_a9_lab_to_prevent_unsafe_yaml_deserialization():
    views = importlib.import_module("introduction.views")

    # The patch replaces yaml.load(..., yaml.Loader) with yaml.safe_load(...)
    # We assert the module now references safe_load and does not reference yaml.load.
    # (We don't execute the view; this is a delta test to ensure the safer API is wired in.)
    assert hasattr(views.yaml, "safe_load")
    # Ensure the function source text includes safe_load.
    import inspect

    src = inspect.getsource(views.a9_lab)
    assert "safe_load" in src
    assert "yaml.load" not in src
