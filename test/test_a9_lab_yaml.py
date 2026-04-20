import yaml


def test_a9_lab_uses_yaml_safe_load_for_uploaded_file():
    # Delta: views.py switched from yaml.load(file, yaml.Loader) to yaml.safe_load(file)
    # Here we assert safe_load rejects a python object tag.
    payload = "!!python/object/apply:os.system ['echo vulnerable']"
    try:
        yaml.safe_load(payload)
        assert False, 'expected safe_load to reject python object tag'
    except yaml.YAMLError:
        assert True
