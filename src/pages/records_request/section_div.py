from pages.element import Element
from pages.records_request.locators import RecordRequestLocators as Locators


class PublicDocs(Element):
    locator = Locators.PUBLIC_DOCS
    id = 'public-docs'


class RequesterDocs(Element):
    locator = Locators.REQUESTER_DOCS
    id = 'requester-docs'
