from selenium.webdriver.common.by import By
import re

class SingupHelper:
    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd

        base_url = self.app.base_url.rstrip('/')
        absolute_url = f"{base_url}/signup_page.php"
        wd.get(absolute_url)


        wd.find_element(By.NAME, "username").send_keys(username)
        wd.find_element(By.NAME, "email").send_keys(email)
        wd.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        wd.get(url)
        wd.find_element(By.NAME, "password").send_keys(password)
        wd.find_element(By.NAME, "password_confirm").send_keys(password)
        wd.find_element(By.CSS_SELECTOR, 'input[value="Update User"]').click()

    def extract_confirmation_url(self, text):
        return re.search("http://.*$", text, re.MULTILINE).group(0)





