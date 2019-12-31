from pages.login.locators import LoginPageLocators
from pages.page import Page
from util.checkbox import check_box
from util.constants import LOGIN_URL


class LoginPage(Page):

    @property
    def url(self):
        return LOGIN_URL

    @property
    def email_field(self):
        return self.driver.find_element(*LoginPageLocators.EMAIL_FIELD)

    @property
    def password_field(self):
        return self.driver.find_element(*LoginPageLocators.PASSWORD_FIELD)

    @property
    def remember_box(self):
        return self.driver.find_element(*LoginPageLocators.REMEMBER_ME_BOX)

    @property
    def submit_button(self):
        return self.driver.find_element(*LoginPageLocators.SUBMIT_BUTTON)

    def login(self, email, password):
        self.visit()
        self.set_email(email)
        self.set_password(password)
        self.remember_me()
        self.submit()

    def set_email(self, email):
        self.email_field.send_keys(email)

    def set_password(self, password):
        self.password_field.send_keys(password)

    def remember_me(self):
        check_box(self.remember_box)

    def submit(self):
        self.submit_button.click()
