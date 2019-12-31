from selenium.webdriver.common.by import By


class RecordRequestLocators:

    ##########
    # common #
    ##########
    LOADER = (By.CLASS_NAME, 'vex-loading-spinner')
    SECTION_HEADER = (By.CLASS_NAME, 'section-header')
    SUBSECTION_TITLE = (By.CLASS_NAME, 'info-title')

    ###########
    # request #
    ###########
    REQUEST_HEADER = (By.CLASS_NAME, 'js-request-pretty-id.t--headline.t--bold')
    REQUEST_INFO = (By.CLASS_NAME, 'request-info-box')
    FILTERED_BY = (By.CLASS_NAME, 'js-requests-filtered-by')
    REQUEST_TEXT = (By.ID, 'request-text')
    REQUEST_DATE = (By.CLASS_NAME, 'request_date')
    CURRENT_DEPARTMENT = (By.CLASS_NAME, 'current-department')
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
    HIDDEN_SECTION = (By.CLASS_NAME, 'row.hide-for-print')
    SECTION_TOGGLE = (By.CLASS_NAME, 'folder-toggle-icon')
    COLLAPSED_TOGGLE = (By.CLASS_NAME, 'fa-caret-right')
    HIDDEN_SECTION_LIST = (By.CLASS_NAME, 'state-requester')
    HIDDEN_SECTION_ITEM = (By.CLASS_NAME, 'CSLAPostingSurvey-requester-toggleable')

    # navigation
    MAIN_NAV = (By.XPATH, '//*[@id="requester-docs"]/nav')
    NAVIGATION = (By.CLASS_NAME, 'pagination')
    NAVIGATION_PAGE = (By.CLASS_NAME, 'page')
    NAVIGATION_ACTIVE = (By.CLASS_NAME, 'page.active')
    NAVIGATION_PREV = (By.CLASS_NAME, 'page.prev')
    NAVIGATION_NEXT = (By.CLASS_NAME, 'page.next')

    ###################
    # request history #
    ###################

    REQUEST_HISTORY = (By.CLASS_NAME, 'request-history')
    REQUEST_HISTORY_SHOW_ALL = (By.CLASS_NAME, 'show-all-history')
    REQUEST_HISTORY_EVENT = (By.CLASS_NAME, 'generic-event')
    REQUEST_HISTORY_EVENT_TITLE = (By.CLASS_NAME, 'event-title')
    REQUEST_HISTORY_EVENT_ITEM = (By.CLASS_NAME, 'event-item')
    REQUEST_HISTORY_EVENT_DATE = (By.CLASS_NAME, 'time-quotes')
