from selenium.webdriver.common.by import By

from pages.locators import Locators


class RecordRequestLocators(Locators):

    ##########
    # common #
    ##########
    SECTION_HEADER = (By.CLASS_NAME, 'section-header')
    SUBSECTION_TITLE = (By.CLASS_NAME, 'info-title')

    ###########
    # request #
    ###########
    REQUEST_HEADER = (By.CLASS_NAME, 'js-request-pretty-id.t--headline.t--bold')
    REQUEST_INFO = (By.CLASS_NAME, 'request-info-box')
    REQUEST_FILTERED_BY = (By.CLASS_NAME, 'js-requests-filtered-by')
    REQUEST_TEXT = (By.ID, 'request-text')
    REQUEST_DATE = (By.CLASS_NAME, 'request_date')
    REQUEST_CURRENT_DEPARTMENT = (By.CLASS_NAME, 'current-department')
    REQUESTER_DETAILS = (By.CLASS_NAME, 'requester-details')

    #############
    # documents #
    #############

    # the main container of document links
    DOCUMENTS = (By.CLASS_NAME, 'document-list')

    DOCUMENTS_PUBLIC_DOCS = (By.ID, 'public-docs')
    DOCUMENTS_REQUESTER_DOCS = (By.ID, 'requester-docs')
    DOCUMENT_ROW = (By.CLASS_NAME, 'row')
    DOCUMENT_LINK = (By.CLASS_NAME, 'document-link')

    # collapsible lists that are hidden by default
    FOLDER = (By.CLASS_NAME, 'row.hide-for-print')
    FOLDER_LIST = (By.CLASS_NAME, 'state-requester')
    FOLDER_ITEM = (By.CLASS_NAME, 'CSLAPostingSurvey-requester-toggleable')
    FOLDER_TOGGLE = (By.CLASS_NAME, 'folder-toggle-icon')
    FOLDER_COLLAPSED_TOGGLE = (By.CLASS_NAME, 'fa-caret-right')

    # navigation
    DOCS_MAIN_NAV = (By.XPATH, '//*[@id="requester-docs"]/nav')  # nav for the main docs div
    DOCS_NAV = (By.CLASS_NAME, 'pagination')  # all navs in the docs div, including folders
    NAV_PAGE = (By.CLASS_NAME, 'page')
    NAV_ACTIVE = (By.CLASS_NAME, 'page.active')
    NAVIGATION_PREV = (By.CLASS_NAME, 'page.prev')
    NAVIGATION_NEXT = (By.CLASS_NAME, 'page.next')

    ###################
    # request history #
    ###################

    REQ_HISTORY = (By.CLASS_NAME, 'request-history')
    REQ_HISTORY_SHOW_ALL = (By.CLASS_NAME, 'show-all-history')
    REQ_HISTORY_EVENT = (By.CLASS_NAME, 'generic-event')
    REQ_HISTORY_EVENT_TITLE = (By.CLASS_NAME, 'event-title')
    REQ_HISTORY_EVENT_ITEM = (By.CLASS_NAME, 'event-item')
    REQ_HISTORY_EVENT_DATE = (By.CLASS_NAME, 'time-quotes')
