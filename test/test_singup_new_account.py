import string
import random

def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_singup_new_account(app):
    app.open_home_page()

    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exists(username, password)
    app.singup.new_user(username, email, password)

    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.logout()