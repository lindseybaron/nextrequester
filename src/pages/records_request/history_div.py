from pages.element import Element
from pages.records_request.locators import RecordRequestLocators as Locators


class RecordRequestHistory(Element):
    locator = Locators.REQ_HISTORY

    @property
    def show_all_toggle(self):
        return self.find_element(*Locators.REQ_HISTORY_SHOW_ALL)

    def event_title(self):
        return self.find_element(*Locators.REQ_HISTORY_EVENT_TITLE)

    def event_item(self):
        return self.find_element(*Locators.REQ_HISTORY_EVENT_ITEM)

    def event_date(self):
        return self.find_element(*Locators.REQ_HISTORY_EVENT_DATE)
