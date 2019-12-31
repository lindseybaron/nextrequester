from pages.element import Element
from pages.records_request.locators import RecordRequestLocators


class RequestInfo(Element):
    locator = RecordRequestLocators.REQUEST_INFO

    @property
    def request_text(self):
        return self.find(RecordRequestLocators.REQUEST_TEXT)

    @property
    def request_date(self):
        return self.find(RecordRequestLocators.REQUEST_DATE)

    @property
    def current_department(self):
        return self.find(RecordRequestLocators.CURRENT_DEPARTMENT)

    @property
    def requester_details(self):
        return self.find(RecordRequestLocators.REQUESTER_DETAILS)
