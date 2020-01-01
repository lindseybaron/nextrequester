import polling

from pages.element import Element
from pages.records_request.locators import RecordRequestLocators as Locators
from util.constants import SELENIUM_SLEEP_INTERVAL, SELENIUM_WAIT_TIME
from util.file import file_exists


class Documents(Element):
    locator = Locators.DOCUMENTS

    @property
    def document_links(self):
        """List of document links visible on the page in its current state.

        Returns:
            List(WebElement): Document links.
        """
        self.wait_for_loaded()
        return self.find_all(Locators.DOCUMENT_LINK)

    @property
    def hidden_sections(self):
        """List of nested (expandable) sections visible on the page in its current state.

        Returns:
            List(WebElement): Nested sections.
        """
        return self.find_all(Locators.HIDDEN_SECTION)

    @property
    def hidden_section_toggle_icons(self):
        """List of toggle icons for nested (expandable) sections visible on the page in its current state.

        Returns:
            List(WebElement): Toggle icons.
        """
        self.wait_for_loaded()
        return self.find_all(Locators.SECTION_TOGGLE)

    @property
    def collapsed_toggles(self):
        """List of collapsed (closed) toggle icons for nested (expandable) sections visible on the page in its current state.

        Returns:
            List(WebElement): Collapsed toggle icons.
        """
        self.wait_for_loaded()
        return self.find_all(Locators.COLLAPSED_TOGGLE)

    @property
    def main_nav(self):
        """Page navigation for the main Documents container.

        Returns:
            WebElement: Nav for main documents.
        """
        navs = self.find_all(Locators.MAIN_NAV)
        if len(navs) > 1:
            raise ValueError
        elif len(navs) > 0:
            return navs[0]

    @property
    def main_nav_next(self):
        """Next button of the page navigation for the main Documents container.

        Returns:
            WebElement: Next link for main documents.
        """
        self.wait_for_loaded()
        if self.main_nav:
            return self.main_nav.find_element(Locators.NAVIGATION_NEXT)

    @property
    def main_nav_active(self):
        """Active page of the page navigation for the main Documents container.

        Returns:
            WebElement: Active page of main documents.
        """
        self.wait_for_loaded()
        if self.main_nav:
            return self.main_nav.find_element(Locators.NAVIGATION_ACTIVE)

    @property
    def main_nav_first(self):
        """First page of the page navigation for the main Documents container.

        Returns:
            WebElement: First page of main documents.
        """
        self.wait_for_loaded()
        if self.main_nav:
            return list(filter(lambda p: p.text == '1', self.main_nav.find_elements(Locators.NAVIGATION_PAGE)))[0]

    @property
    def main_active_next_link(self):
        """Active Next links for the main Documents container.

        Returns:
            WebElement: Active Next link for main Documents.
        """
        self.wait_for_loaded()
        next_links = self.main_nav.find_elements(*Locators.NAVIGATION_NEXT)
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
        for section in self.hidden_sections:
            section_next_links.update(section.find_elements(*Locators.NAVIGATION_NEXT))
        return [link for link in section_next_links if 'disabled' not in link.get_attribute('class')]

    @staticmethod
    def download_missing(links, downloaded, req_id=None):
        for link in links:
            if not file_exists(link.text, request_id=req_id) and link.get_attribute('href') not in downloaded:
                link.click()
                downloaded.add(link.get_attribute('href'))

        return downloaded

    def wait_for_loaded(self):
        """Wait until the documents section of the page has finished loading.

        Returns:
            bool: True if loading has completed.
        """
        polling.poll(
            lambda: 'loading' not in self.text,
            step=SELENIUM_SLEEP_INTERVAL,
            timeout=SELENIUM_WAIT_TIME,
        )
        return True

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

    def download_files(self, req_id=None):
        self.wait_for_loaded()
        self.expand_all_toggles()
        self.wait_for_loaded()

        links = set(self.document_links)
        downloaded = self.download_missing(links, set(), req_id=req_id)

        # while active next links exists, click the first one and add any new links to set
        while self.main_active_next_link:
            while self.nest_active_next_links:
                self.wait_for_loaded()
                self.nest_active_next_links[0].click()
                self.wait_for_loaded()
                self.expand_all_toggles()
                self.wait_for_loaded()
                downloaded = self.download_missing(links=self.document_links, downloaded=downloaded, req_id=req_id)
            self.wait_for_loaded()
            self.main_active_next_link.click()
            self.wait_for_loaded()
            self.expand_all_toggles()
            self.wait_for_loaded()
            downloaded = self.download_missing(links=self.document_links, downloaded=downloaded, req_id=req_id)


