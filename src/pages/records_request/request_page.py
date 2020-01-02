from pages.records_request.documents_div import RecordRequestDocuments
from pages.page import Page
from pages.records_request.history_div import RecordRequestHistory
from pages.records_request.locators import RecordRequestLocators as Locators
from pages.records_request.info_div import RecordRequestInfo
from util.constants import REQUEST_URL


class RecordRequestPage(Page):

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.request_id = kwargs.get('request_id')

    @property
    def url(self):
        return REQUEST_URL.format(request_id=self.request_id)

    @property
    def loader(self):
        return self.driver.find_element(*Locators.LOADER)

    @property
    def request_header(self):
        return self.driver.find_element(*Locators.REQUEST_HEADER)

    @property
    def filtered_by(self):
        return self.driver.find_element(*Locators.REQUEST_FILTERED_BY)

    @property
    def request_info(self):
        return RecordRequestInfo(self.driver)

    @property
    def documents(self):
        return RecordRequestDocuments(self.driver)

    @property
    def history(self):
        return RecordRequestHistory(self.driver)

    def download_all_files(self):
        self.documents.download_files(sub_dir=self.request_id)
