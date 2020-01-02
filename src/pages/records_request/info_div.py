from pages.element import Element
from pages.records_request.locators import RecordRequestLocators as Locators


class RecordRequestInfo(Element):
    locator = Locators.REQUEST_INFO

    @property
    def request_text(self):
        return self.find_element(*Locators.REQUEST_TEXT)

    @property
    def request_date(self):
        return self.find_element(*Locators.REQUEST_DATE)

    @property
    def current_department(self):
        return self.find_element(*Locators.REQUEST_CURRENT_DEPARTMENT)

    @property
    def requester_details(self):
        return self.find_element(*Locators.REQUESTER_DETAILS)
