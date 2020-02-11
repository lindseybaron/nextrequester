import polling
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from pages.locators import Locators
from util.constants import WAIT_TIME, WAIT_INTERVAL, LONG_WAIT_TIME


class Element:
    locator = ()

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
        return WebDriverWait(self.driver, WAIT_TIME).until(
            ec.visibility_of_element_located(self.locator))

    def get_all(self):
        return WebDriverWait(self.driver, WAIT_TIME).until(
            ec.visibility_of_any_elements_located(self.locator))

    def find_element(self, by, locator):
        _self = self.driver.find_element(*self.locator)
        return _self.find_element(by, locator)

    def find_elements(self, by, locator):
        _self = self.driver.find_element(*self.locator)
        return _self.find_elements(by, locator)

    def find_element_by_text(self, text):
        _self = self.driver.find_element(*self.locator)
        xpath = '//*[text()="{}"]'.format(text)
        return _self.find_element(By.XPATH, xpath)

    def find_children(self):
        _self = self.driver.find_element(*self.locator)
        return _self.find_elements(*Locators.CHILDREN)

    def wait_for_loaded(self):
        """Wait until this element has finished loading.

        Returns:
            bool: True if loading has completed.
        """
        polling.poll(
            lambda: 'loading' not in self.text and len(self.find_elements(*Locators.LOADER)) < 1,
            step=WAIT_INTERVAL,
            timeout=LONG_WAIT_TIME,
        )
        return True
