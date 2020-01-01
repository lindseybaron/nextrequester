from selenium.webdriver.common.by import By

from pages.login.login_page import LoginPage
from util.config import load_user, get_secret
from util.driver import get_driver


class TestLogin:

    def test_login(self):
        user = load_user(email=get_secret('email'), pw=get_secret('pw'))
        driver = get_driver()
        LoginPage(driver).login(user['email'], user['pw'])

        message = driver.find_element(By.CLASS_NAME, 'alert-bar.alert-bar--primary').text
        assert 'signed in' in message
