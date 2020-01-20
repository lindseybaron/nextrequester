from selenium.webdriver.common.by import By

from pages.element import Element
from pages.records_request.locators import RecordRequestLocators as Locators
from pages.records_request.section_div import PublicDocs, RequesterDocs
from util.file import file_exists


class RecordRequestDocuments(Element):
    locator = Locators.DOCUMENTS

    @property
    def document_links(self):
        """List of document links visible on the page in its current state.

        Returns:
            List(WebElement): Document links.
        """
        self.wait_for_loaded()
        return self.find_elements(*Locators.DOCUMENT_LINK)

    @property
    def doc_box(self):
        return self.find_element(*Locators.DOCUMENTS_BOX)

    @property
    def public_docs(self):
        return PublicDocs(self.driver)

    @property
    def requester_docs(self):
        return RequesterDocs(self.driver)

    @property
    def doc_sections(self):
        self.wait_for_loaded()
        sections = []
        if self.public_docs:
            sections.append(self.public_docs)
        if self.requester_docs:
            sections.append(self.requester_docs)
        return sections

    @property
    def folders(self):
        """List of nested (expandable) sections visible on the page in its current state.

        Returns:
            List(WebElement): Nested sections.
        """
        return self.find_elements(*Locators.FOLDER)

    @property
    def collapsed_toggles(self):
        """List of collapsed (closed) toggle icons for nested (expandable) sections visible on the page in its current state.

        Returns:
            List(WebElement): Collapsed toggle icons.
        """
        self.wait_for_loaded()
        return self.find_elements(*Locators.FOLDER_COLLAPSED_TOGGLE)

    @property
    def main_nav(self):
        """Page navigation for the main Documents container.

        Returns:
            WebElement: Nav for main documents.
        """
        navs = self.find_elements(*Locators.DOCS_REQUESTER_PAGY)
        if len(navs) > 1:
            raise ValueError
        elif len(navs) > 0:
            return navs[0]

    @property
    def main_active_next_link(self):
        """Active Next links for the main Documents container.

        Returns:
            WebElement: Active Next link for main Documents.
        """
        self.wait_for_loaded()
        next_links = self.main_nav.find_elements(*Locators.PAGY_NEXT)
        active_links = list(filter(lambda n: 'disabled' not in n.get_attribute('class'), next_links))
        if active_links:
            return active_links[0]

    @property
    def nest_active_next_links(self):
        """List of active Next links for nested subsections currently visible on the page.

        Returns:
            List(WebElement): Active Next links for nested document sections.
        """
        self.wait_for_loaded()
        section_next_links = set()
        for section in self.folders:
            section_next_links.update(section.find_elements(*Locators.PAGY_NEXT))
        return [link for link in section_next_links if 'disabled' not in link.get_attribute('class')]

    @staticmethod
    def download_missing(links, downloaded, sub_dir=None):
        for link in links:
            if not file_exists(link, sub_dir=sub_dir) and link.get_attribute('href') not in downloaded:
                # Note: this only prevents duplicate downloads in the current run.
                # If the file already existed prior to running the command, it may still download it.
                link.click()
                downloaded.add(link.get_attribute('href'))

        return downloaded

    def expand_toggle(self, toggle):
        self.wait_for_loaded()
        if 'fa-caret-right' in toggle.get_attribute('class'):
            toggle.click()

    def has_collapsed_toggles(self):
        self.wait_for_loaded()
        return len(self.collapsed_toggles) > 0

    def expand_all_toggles(self):
        self.wait_for_loaded()
        while self.has_collapsed_toggles():
            [self.expand_toggle(toggle) for toggle in self.collapsed_toggles]

    def download_files(self, sub_dir=None):
        self.wait_for_loaded()
        self.expand_all_toggles()
        self.wait_for_loaded()

        links = set(self.document_links)
        downloaded = self.download_missing(links, set(), sub_dir=sub_dir)

        # while active next links exists, click the first one and add any new links to set
        while self.main_active_next_link:
            while self.nest_active_next_links:
                self.wait_for_loaded()
                self.nest_active_next_links[0].click()
                self.wait_for_loaded()
                self.expand_all_toggles()
                self.wait_for_loaded()
                downloaded = self.download_missing(links=self.document_links, downloaded=downloaded, sub_dir=sub_dir)
            self.wait_for_loaded()
            self.main_active_next_link.click()
            self.wait_for_loaded()
            self.expand_all_toggles()
            self.wait_for_loaded()
            downloaded = self.download_missing(links=self.document_links, downloaded=downloaded, sub_dir=sub_dir)
