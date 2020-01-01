from pages.records_request.documents import Documents
from pages.page import Page
from pages.records_request.history import RequestHistory
from pages.records_request.locators import RecordRequestLocators
from pages.records_request.request_info import RequestInfo
from util.constants import REQUEST_URL


class RequestPage(Page):

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.request_id = kwargs.get('request_id')

    @property
    def url(self):
        return REQUEST_URL.format(request_id=self.request_id)

    @property
    def loader(self):
        return self.driver.find_element(*RecordRequestLocators.LOADER)

    @property
    def request_header(self):
        return self.driver.find_element(*RecordRequestLocators.REQUEST_HEADER)

    @property
    def filtered_by(self):
        return self.driver.find_element(*RecordRequestLocators.FILTERED_BY)

    @property
    def request_info(self):
        return RequestInfo(self.driver)

    @property
    def documents(self):
        return Documents(self.driver)

    @property
    def history(self):
        return RequestHistory(self.driver)

    def download_all_files(self):
        self.documents.download_files(req_id=self.request_id)
