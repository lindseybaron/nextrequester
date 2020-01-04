import os

from pages.documents.docs_header import DocumentsHeader
from pages.documents.docs_list_div import DocumentsList
from pages.documents.docs_pagy import DocumentsPagination
from pages.documents.docs_search_form import DocumentsSearchForm
from pages.documents.locators import DocumentsLocators as Locators
from pages.page import Page
from util.constants import DOCUMENTS_URL
from util.file import get_download_dir
from util.wait import wait_until


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

    def visit_with_params(self, page=None, per_page=None):
        url = self.build_url(page=page, per_page=per_page)

        self.driver.get(url)
        wait_until(self.is_loaded())

    def build_url(self, page=None, per_page=None):
        _params = []
        if page:
            _params.append('documents_smart_listing[page]={}'.format(page))
        if per_page:
            _params.append('documents_smart_listing[per_page]={}'.format(per_page))
        _params.append('documents_smart_listing[sort][count]=desc')

        params = "&".join(_params)
        return '{}?{}'.format(self.url, params)

    def is_loaded(self):
        return self.documents.is_loaded()

    def has_pagy(self):
        return len(self.driver.find_elements(*Locators.DOCS_PAGY)) > 0

    def show_most(self):
        if self.has_pagy():
            if self.pagination.has_show_per_page():
                self.pagination.per_page_picker.show_most()

    def download_results(self, results):
        print('Downloading {} results...'.format(len(results)))
        for result in results:
            dl_dir = os.path.join(get_download_dir(), 'documents')
            dl_path = os.path.join(dl_dir, result['filename'].replace('/', '-'))
            url = result['doc_url'] + '/download?token='
            print('Downloading {} to {}...'.format(url, dl_path))
            response = self.driver.request('GET', url)
            with open(dl_path, 'wb') as f:
                f.write(response.content)
