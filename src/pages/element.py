from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from util.constants import SELENIUM_WAIT_TIME


class Element:

    def __init__(self, driver, locator=None, **kwargs):
        self.driver = driver
        if not self.locator and locator:
            self.locator = locator

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def text(self):
        return self.get().text

    def get(self):
        return WebDriverWait(self.driver, SELENIUM_WAIT_TIME).until(
            ec.visibility_of_element_located(self.locator))

    def get_all(self):
        return WebDriverWait(self.driver, SELENIUM_WAIT_TIME).until(
            ec.visibility_of_any_elements_located(self.locator))

    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)
