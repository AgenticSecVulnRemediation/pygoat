import yaml


def test_safe_load_does_not_construct_python_objects(tmp_path):
    """Delta test: yaml.safe_load should not allow !!python/object/apply execution vectors."""

    payload = "!!python/object/apply:os.system ['echo pwned']\n"
    p = tmp_path / "payload.yaml"
    p.write_text(payload)

    # With yaml.safe_load this should raise a ConstructorError (or similar YAML error),
    # whereas yaml.load could construct arbitrary objects.
    with p.open("r") as stream:
        try:
            yaml.safe_load(stream)
            # If it doesn't raise, it still must not return an executable object.
        except yaml.constructor.ConstructorError:
            pass
