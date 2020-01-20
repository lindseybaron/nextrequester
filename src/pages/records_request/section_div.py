from selenium.webdriver.common.by import By

from pages.records_request.locators import RecordRequestLocators as Locators

from pages.element import Element


class DocumentsSection(Element):
    id = ''
    folders_xpath = '//*[@id="{}"]/div/div[2]/div[{}]'

    @property
    def doc_links(self):
        return self.find_elements(*Locators.DOCUMENT_LINK)

    @property
    def folders(self):
        return self.find_elements(*Locators.FOLDER)

    @property
    def pagy(self):
        _pagys = self.find_elements(By.XPATH, '//*[@id="{}"]/nav'.format(self.id))
        if len(_pagys) == 1:
            return self.find_element(By.XPATH, '//*[@id="{}"]/nav'.format(self.id))

    @property
    def has_active_next(self):
        next_link = self.pagy.find_element(By.CLASS_NAME, 'page.next')
        return 'disabled' not in next_link.get_attribute('class')


class PublicDocs(DocumentsSection):
    locator = Locators.PUBLIC_DOCS
    id = 'public-docs'


class RequesterDocs(DocumentsSection):
    locator = Locators.REQUESTER_DOCS
    id = 'requester-docs'
