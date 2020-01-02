import os

from pages.documents.docs_header import DocumentsHeader
from pages.documents.docs_list_div import DocumentsList
from pages.documents.docs_pagy import DocumentsPagination
from pages.documents.docs_search_form import DocumentsSearchForm
from pages.documents.locators import DocumentsLocators as Locators
from pages.page import Page
from util.constants import DOCUMENTS_URL
from util.file import get_download_dir


class DocumentsPage(Page):

    @property
    def url(self):
        return DOCUMENTS_URL

    @property
    def header(self):
        return DocumentsHeader(self.driver)

    @property
    def search_form(self):
        return DocumentsSearchForm(self.driver)

    @property
    def documents(self):
        return DocumentsList(self.driver)

    @property
    def pagination(self):
        return DocumentsPagination(self.driver)

    def has_pagy(self):
        return len(self.driver.find_elements(*Locators.DOCS_PAGY)) > 0

    def download_results(self, results):
        for result in results:
            dl_dir = os.path.join(get_download_dir(), 'documents')
            dl_path = os.path.join(dl_dir, result['filename'].replace('/', '-'))
            url = result['doc_url'] + '/download?token='
            print('Downloading {} to {}...'.format(url, dl_path))
            response = self.driver.request('GET', url)
            with open(dl_path, 'wb') as f:
                f.write(response.content)

    def download_all_files(self):
        # get rows from first page
        self.download_results(self.documents.get_visible_results())
        # check for pagination
        if self.has_pagy() and self.pagination.has_next_page():
            # iterate over pages and get rows from each page
            current_page = 1
            # show max results per page
            if self.pagination.has_show_per_page():
                self.pagination.per_page_picker.show_most()

            page_count = self.pagination.get_page_count()
            while current_page < page_count:
                self.pagination.go_to_next_page()
                print('Getting results for page {}...'.format(self.pagination.current_page.text))
                self.download_results(self.documents.get_visible_results())

                current_page = int(self.pagination.current_page.text)
