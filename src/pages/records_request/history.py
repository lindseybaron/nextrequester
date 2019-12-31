from pages.element import Element
from pages.records_request.locators import RecordRequestLocators as Locators


class RequestHistory(Element):
    locator = Locators.REQUEST_HISTORY

    @property
    def show_all_toggle(self):
        return self.find(Locators.REQUEST_HISTORY_SHOW_ALL)

    def event_title(self):
        return self.find(Locators.REQUEST_HISTORY_EVENT_TITLE)

    def event_item(self):
        return self.find(Locators.REQUEST_HISTORY_EVENT_ITEM)

    def event_date(self):
        return self.find(Locators.REQUEST_HISTORY_EVENT_DATE)
