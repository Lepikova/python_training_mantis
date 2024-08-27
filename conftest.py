import os
import json
import pytest
import ftputil
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
    """Создает экземпляр приложения."""
    global fixture
    config = load_config(request.config.getoption("--target"))
    web_config = config['web']
    browser = request.config.getoption("--browser")
    base_url = web_config['baseUrl']
    fixture = Application(browser=browser, base_url=base_url, config=config)

    # Добавляем финализатор для завершения сессии
    def fin():
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


@pytest.fixture(scope="function")
def ensure_login(app, request):
    """Обеспечивает, что пользователь авторизован перед каждым тестом."""
    config = load_config(request.config.getoption("--target"))
    webadmin_config = config['webadmin']
    username = webadmin_config['username']
    password = webadmin_config['password']

    app.session.ensure_login(username, password)

@pytest.fixture(scope="session", autouse=True)
def configure_server(request):
    config = load_config(request.config.getoption("--target"))
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)



def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")