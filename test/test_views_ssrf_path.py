import os
import types


def test_ssrf_lab_blocks_path_traversal_by_base_dir_prefix(monkeypatch):
    """Delta test: ssrf_lab in introduction/views.py now blocks path traversal using a base_dir prefix check."""

    import introduction.views as views

    # Force a predictable __file__ base for views.py
    fake_dir = os.path.abspath(os.path.join(os.getcwd(), "introduction"))
    monkeypatch.setattr(views, "__file__", os.path.join(fake_dir, "views.py"))

    opened = {"called": False}

    def fake_open(path, mode="r", *args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() should not be called for invalid traversal paths")

    monkeypatch.setattr(views, "open", fake_open, raising=False)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"blog": "../secret.txt"}

    # render returns the context for assertion
    monkeypatch.setattr(views, "render", lambda request, template, context=None: context)

    ctx = views.ssrf_lab(DummyRequest())

    assert opened["called"] is False
    assert ctx == {"blog": "Invalid file path"}
