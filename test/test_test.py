import yaml


def test_yaml_safe_load_is_used_for_untrusted_input():
    # Delta: yaml.safe_load should reject !!python/object tags
    payload = "!!python/object/apply:os.system ['echo pwned']"
    try:
        yaml.safe_load(payload)
    except Exception:
        assert True
    else:
        # If it didn't raise, it must not have executed anything; safe_load should not construct this.
        assert False, "yaml.safe_load unexpectedly loaded a potentially unsafe tag"
