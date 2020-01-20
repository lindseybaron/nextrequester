from selenium.webdriver.common.by import By

from pages.locators import Locators


class RecordRequestLocators(Locators):

    REQUEST_HEADER = (By.CLASS_NAME, 'js-request-pretty-id.t--headline.t--bold')

    #############
    # documents #
    #############

    # the main container of document links
    DOCUMENTS = (By.CLASS_NAME, 'document-list')

    PUBLIC_DOCS = (By.ID, 'public-docs')
    REQUESTER_DOCS = (By.ID, 'requester-docs')
    DOCUMENTS_BOX = (By.CLASS_NAME, 'js-doc-box')
    DOCUMENTS_SECTION = (By.CLASS_NAME, 'js-docs-list')
    DOCUMENT_LINK = (By.CLASS_NAME, 'document-link')

    # collapsible folders with file lists that are hidden by default
    FOLDER = (By.CLASS_NAME, 'row.hide-for-print')
    FOLDER_LIST = (By.CLASS_NAME, 'state-requester')
    FOLDER_ITEM = (By.CLASS_NAME, 'CSLAPostingSurvey-requester-toggleable')
    FOLDER_TOGGLE = (By.CLASS_NAME, 'folder-toggle-icon')
    FOLDER_NAME = (By.CSS_SELECTOR, 'span.font-size-14')
    FOLDER_COLLAPSED_TOGGLE = (By.CLASS_NAME, 'fa-caret-right')

    # navigation
    DOCS_REQUESTER_PAGY = (By.XPATH, '//*[@id="requester-docs"]/nav')  # nav for the main requester docs div
    PAGY = (By.CLASS_NAME, 'pagy-nav')
    PAGY_ACTIVE = (By.CLASS_NAME, 'page.active')
    PAGY_PREV = (By.CLASS_NAME, 'page.prev')
    PAGY_NEXT = (By.CLASS_NAME, 'page.next')
