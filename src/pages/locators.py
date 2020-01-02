from selenium.webdriver.common.by import By


class Locators:
    CHILDREN = (By.XPATH, './/*')
    LINK = (By.TAG_NAME, 'a')
    LOADER = (By.CLASS_NAME, 'vex-loading-spinner')
