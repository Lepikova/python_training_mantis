def test_login(app, ensure_login):
    assert app.session.is_logged_in_as("administrator")