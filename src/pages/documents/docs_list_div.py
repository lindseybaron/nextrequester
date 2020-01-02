import re

import polling

from pages.documents.locators import DocumentsLocators as Locators
from pages.element import Element


class DocumentsList(Element):
    locator = Locators.DOCS_LIST

    @property
    def result_count(self):
        return self.find_element(*Locators.LIST_COUNT)

    @property
    def result_rows(self):
        return self.find_elements(*Locators.LIST_ROW)

    def is_loaded(self):
        loading_div = self.find_element(*Locators.DOCS_LOADING)
        style = loading_div.get_attribute('style')
        if not style:
            return True
        elif 'opacity' in style:
            opacity = [o for o in style.split('; ') if re.search('opacity', o)][0].split(': ')[1]
            return opacity == '0'

    def get_visible_results(self):
        results = []
        self.wait_for_loaded()
        polling.poll(
            lambda: self.is_loaded(),
            step=1,
            timeout=30,
        )

        for row in self.result_rows:
            doc_url = row.find_element(*Locators.ROW_DOC_LINK).get_attribute('href')
            filename = row.find_element(*Locators.ROW_DOC_LINK).text
            print('[ File: {} | URL: {} ]'.format(filename, doc_url))
            results.append({
                'doc_url': doc_url,
                'filename': filename,
            })

        return results
