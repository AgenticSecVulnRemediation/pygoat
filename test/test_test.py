import yaml


def test_yaml_safe_load_rejects_python_object_tags():
    # This payload would be dangerous with yaml.load(Loader=yaml.Loader) in some setups.
    payload = "!!python/object/apply:os.system ['echo vulnerable']"

    # yaml.safe_load should raise an error for unknown constructors.
    try:
        yaml.safe_load(payload)
        assert False, 'expected safe_load to reject python object tag'
    except yaml.YAMLError:
        assert True
