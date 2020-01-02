import re

from bs4 import BeautifulSoup as bs

from pages.documents.locators import DocumentsLocators as Locators
from pages.element import Element
from util.wait import wait_until


class DocumentsList(Element):
    locator = Locators.DOCS_LIST

    @property
    def result_count(self):
        return self.find_element(*Locators.LIST_COUNT)

    @property
    def result_rows(self):
        rows = self.find_elements(*Locators.LIST_ROW)
        print('Found {} rows.'.format(len(rows)))
        return rows

    def is_loaded(self):
        loading_div = self.find_element(*Locators.DOCS_LOADING)
        style = loading_div.get_attribute('style')
        link_count = len(self.find_elements(*Locators.ROW_DOC_LINK))
        row_count = len(self.find_elements(*Locators.LIST_ROW))
        if not style:
            return link_count == row_count
        elif 'opacity' in style:
            opacity = [o for o in style.split('; ') if re.search('opacity', o)][0].split(': ')[1]
            return opacity == '0' and link_count == row_count

    def get_visible_results(self):
        results = []
        self.wait_for_loaded()
        wait_until(self.is_loaded())

        print('loaded')

        for row in self.result_rows:
            doc_url = row.find_element(*Locators.ROW_DOC_LINK).get_attribute('href')

            # get the full filename from the doc page, because the list tends to cut them off
            doc_response = self.driver.request('GET', doc_url)
            filename = bs(doc_response.content, 'html.parser').select('div.published')[0].get_text().strip()

            print('[ File: {} | URL: {} ]'.format(filename, doc_url))
            results.append({
                'doc_url': doc_url,
                'filename': filename,
            })

        return results
