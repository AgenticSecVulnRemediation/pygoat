import pytest


@pytest.mark.django_db
def test_ssrf_lab_rejects_non_whitelisted_blog_key(mocker):
    """Regression: path traversal fix only allows whitelisted blog identifiers."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"blog": "../../etc/passwd"}

    render_spy = mocker.spy(views, "render")

    # Act
    response = views.ssrf_lab(DummyRequest())

    # Assert: should not attempt to open any file; should render error message
    assert response.status_code == 200
    assert render_spy.call_args[0][1] == "Lab/ssrf/ssrf_lab.html"
    assert render_spy.call_args[0][2]["blog"] == "Invalid blog identifier"


@pytest.mark.django_db
def test_ssrf_lab_opens_only_whitelisted_filename(mocker, monkeypatch):
    """Regression: whitelisted key is mapped to safe filename and opened via context manager."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"blog": "blog1"}

    opened = {}

    def fake_open(path, mode):
        opened["path"] = path
        opened["mode"] = mode

        class CM:
            def __enter__(self):
                class F:
                    def read(self_inner):
                        return "hello"
                return F()

            def __exit__(self, exc_type, exc, tb):
                return False

        return CM()

    monkeypatch.setattr(views, "open", fake_open)

    render_spy = mocker.spy(views, "render")

    # Act
    response = views.ssrf_lab(DummyRequest())

    # Assert
    assert response.status_code == 200
    assert opened["mode"] == "r"
    assert opened["path"].endswith("blog1.txt")
    assert render_spy.call_args[0][2]["blog"] == "hello"
