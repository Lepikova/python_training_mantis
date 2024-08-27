from selenium import webdriver

from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from selenium.webdriver.common.by import By
from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.singup import SingupHelper
from fixture.soap import SoapHelper

class Application:

    def __init__(self, browser, base_url, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.singup = SingupHelper(self)
        self.mail = MailHelper(self)
        self.base_url = base_url
        self.config = config
        self.soap = SoapHelper(self)


    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)
    def return_to_home_page(self):
        wd = self.wd
        # return to home page
        wd.find_element(By.LINK_TEXT, "My View").click()
    def destroy(self):
        self.wd.quit()