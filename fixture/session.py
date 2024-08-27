from selenium.webdriver.common.by import By

class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        # Открываем главную страницу
        self.app.open_home_page()
        # Вводим имя пользователя
        wd.find_element(By.NAME, "username").click()
        wd.find_element(By.NAME, "username").clear()
        wd.find_element(By.NAME, "username").send_keys(username)
        # Вводим пароль
        wd.find_element(By.NAME, "password").click()
        wd.find_element(By.NAME, "password").clear()
        wd.find_element(By.NAME, "password").send_keys(password)
        # Нажимаем кнопку отправки формы
        wd.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    def logout(self):
        wd = self.app.wd
        # Нажимаем на ссылку выхода
        wd.find_element(By.LINK_TEXT, "Logout").click()

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        # Получаем имя залогиненного пользователя
        return wd.find_element(By.CSS_SELECTOR, "td.login-info-left span").text

    def is_logged_in(self):
        wd = self.app.wd
        # Проверяем, залогинен ли пользователь
        return len(wd.find_elements(By.LINK_TEXT, "Logout")) > 0

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)