from fixture.application import Application
import pytest
import json
import os.path

import pytest
import json
import os.path
from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def app(request):
    global fixture
    config = load_config(request.config.getoption("--target"))
    web_config = config['web']
    webadmin_config = config['webadmin']

    browser = request.config.getoption("--browser")
    fixture = Application(browser=browser, base_url=web_config['baseUrl'])

    # Выполняем вход в систему
    username = webadmin_config['username']
    password = webadmin_config['password']
    fixture.session.ensure_login(username, password)

    # Добавляем финализатор для разлогинивания и завершения сессии
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
