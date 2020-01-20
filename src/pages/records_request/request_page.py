import polling
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

from pages.page import Page
from pages.records_request.documents_div import RecordRequestDocuments
from pages.records_request.locators import RecordRequestLocators as Locators
from util.constants import REQUEST_URL, SELENIUM_SLEEP_INTERVAL, SELENIUM_WAIT_TIME
from util.wait import wait_until


class RecordRequestPage(Page):

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.request_id = kwargs.get('request_id')

    @property
    def url(self):
        return REQUEST_URL.format(request_id=self.request_id)

    @property
    def loader(self):
        _loaders = self.driver.find_elements(*Locators.LOADER)
        if len(_loaders) > 0:
            return _loaders[0]

    @property
    def request_header(self):
        return self.driver.find_element(*Locators.REQUEST_HEADER)

    @property
    def documents(self):
        return RecordRequestDocuments(self.driver)

    @staticmethod
    def has_active_next(pagy):
        next_link = pagy.find_element(By.CLASS_NAME, 'page.next')
        return 'disabled' not in next_link.get_attribute('class')

    def is_loaded(self):
        polling.poll(
            lambda: 'loading' not in self.documents.text and not self.loader,
            step=SELENIUM_SLEEP_INTERVAL,
            timeout=SELENIUM_WAIT_TIME,
        )
        return True

    @staticmethod
    def parse_link_data(link_elements):
        return [{'url': l.get_attribute('href'), 'filename': l.text.strip()} for l in link_elements]

    def get_folder_doc_urls(self, section):
        link_data = []
        # expand the folders
        for folder in section.folders:
            folder.find_element(*Locators.FOLDER_TOGGLE).click()
            self.documents.wait_for_loaded()
            link_data.extend(self.parse_link_data(folder.find_elements(*Locators.DOCUMENT_LINK)))

            if len(folder.find_elements(*Locators.PAGY)) > 0:
                next_link = folder.find_element(*Locators.PAGY).find_element(By.CLASS_NAME, 'page.next')
                while 'disabled' not in next_link.get_attribute('class'):
                    folder.find_element(*Locators.PAGY).find_element(By.CLASS_NAME, 'page.next').click()
                    self.documents.wait_for_loaded()
                    link_data.extend(self.parse_link_data(folder.find_elements(*Locators.DOCUMENT_LINK)))
                    next_link = folder.find_element(*Locators.PAGY).find_element(By.CLASS_NAME, 'page.next')

        return link_data

    def collect_all_document_urls(self):
        link_data = []

        for section in self.documents.doc_sections:
            link_data.extend(self.parse_link_data(section.doc_links))
            link_data.extend(self.get_folder_doc_urls(section))

            if section.pagy:
                while section.has_active_next:
                    section.pagy.find_element(By.CLASS_NAME, 'next').click()
                    self.documents.wait_for_loaded()
                    link_data.extend(self.parse_link_data(section.doc_links))
                    link_data.extend(self.get_folder_doc_urls(section))

        return link_data
