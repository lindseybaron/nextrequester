from selenium.webdriver.common.by import By

from pages.locators import Locators


class LoginPageLocators(Locators):

    LOGIN_FORM = (By.ID, 'new_user')
    EMAIL_FIELD = (By.ID, 'user_email')
    PASSWORD_FIELD = (By.ID, 'user_password')
    REMEMBER_ME_BOX = (By.CLASS_NAME, 'checkbox.js-checkbox')
    SUBMIT_BUTTON = (By.CLASS_NAME, 'js-submit')
    FORGOT_LINK = (By.PARTIAL_LINK_TEXT, 'Lost password')
