import polling
import math

from pages.element import Element
from pages.documents.locators import DocumentsLocators as Locators
from util.constants import SELENIUM_SLEEP_INTERVAL, SELENIUM_WAIT_TIME


class DocumentsPagination(Element):
    locator = Locators.DOCS_PAGY

    @property
    def count(self):
        return self.find_element(*Locators.PAGY_RESULT_COUNT)

    @property
    def per_page_picker(self):
        return DocumentsPerPage(self.driver)

    @property
    def current_page(self):
        return self.find_element(*Locators.PAGY_CURRENT_PAGE)

    def has_show_per_page(self):
        return len(self.find_elements(*Locators.PAGY_PER_PAGE)) > 0

    def get_page_count(self):
        return math.ceil(int(self.count.text) / int(self.per_page_picker.current_per_page.text))

    def has_next_page(self):
        return len(self.driver.find_elements(*Locators.PAGY_NEXT_PAGE)) > 0

    def go_to_next_page(self):
        start_page = int(self.current_page.text)
        next_page = start_page + 1
        self.find_element_by_text(next_page).click()
        self.wait_for_loaded()
        polling.poll(
            lambda: int(self.current_page.text) == start_page + 1,
            step=SELENIUM_SLEEP_INTERVAL,
            timeout=SELENIUM_WAIT_TIME,
        )


class DocumentsPerPage(Element):
    locator = Locators.PAGY_PER_PAGE

    @property
    def options(self):
        options = []
        for child in self.find_children():
            if child.tag_name == 'a':
                options.append(child)
            elif child.tag_name == 'span' and 'count' not in child.get_attribute('class'):
                options.append(child)

        return options

    @property
    def current_per_page(self):
        for option in self.options:
            if 'span' in option.tag_name:
                return option

    def show_most(self):
        opts = self.options
        opts.sort(key=lambda x: int(x.text), reverse=True)
        opt_text = opts[0].text
        opts[0].click()
        polling.poll(
            lambda: self.find_element_by_text(opt_text).get_attribute('href') is None,
            step=SELENIUM_SLEEP_INTERVAL,
            timeout=SELENIUM_WAIT_TIME,
        )
