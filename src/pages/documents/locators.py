from selenium.webdriver.common.by import By

from pages.locators import Locators


class DocumentsLocators(Locators):

    ##########
    # header #
    ##########

    DOCS_HEADER = (By.CLASS_NAME, 'pageHeader')

    ##########
    # search #
    ##########

    DOCS_SEARCH_FORM = (By.CSS_SELECTOR, 'div.columns.hide-for-print > ul')

    ########
    # list #
    ########

    DOCS_LIST = (By.ID, 'documents')
    DOCS_LOADING = (By.CLASS_NAME, 'loading')

    LIST_HEADER = (By.CLASS_NAME, 'row.xlight-gray-back')
    LIST_COUNT = (By.CLASS_NAME, 't--title.t--bold')
    LIST_ROW = (By.CLASS_NAME, 'demo-data-false')

    # row
    ROW_DOC_LINK = (By.CLASS_NAME, 'document.published')
    ROW_REQUEST = (By.CSS_SELECTOR, 'td:nth-child(6)')

    ##############
    # pagination #
    ##############

    DOCS_PAGY = (By.CLASS_NAME, 'pagination-centered')

    PAGY_RESULT_COUNT = (By.CLASS_NAME, 'count')
    PAGY_PER_PAGE = (By.CLASS_NAME, 'pagination-per-page')
    PAGY_CURRENT_PAGE = (By.CLASS_NAME, 'page.active')
    PAGY_NEXT_PAGE = (By.CSS_SELECTOR, 'li.next_page > a')
