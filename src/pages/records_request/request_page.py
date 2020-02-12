import polling
from selenium.webdriver.common.by import By

from pages.page import Page
from pages.records_request.documents_div import RecordRequestDocuments
from pages.records_request.locators import RecordRequestLocators as Locators
from util.constants import REQUEST_URL, WAIT_INTERVAL, LONG_WAIT_TIME
from util.find import flaky_find
from util.print import print_pagy


class RecordRequestPage(Page):

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.request_id = kwargs.get('request_id')

    @property
    def url(self):
        """URL of the current records request page.

        Returns:
            str: Full URL of the records request page.
        """
        return REQUEST_URL.format(request_id=self.request_id)

    @property
    def loader(self):
        """Spinning loader element that indicates the page is still loading.

        Returns:
            WebElement: Loader element.
        """
        _loaders = self.driver.find_elements(*Locators.LOADER)
        if len(_loaders) > 0:
            return _loaders[0]

    @property
    def documents(self):
        """The Documents section of the records request page.

        Returns:
            WebElement: Documents div.
        """
        return RecordRequestDocuments(self.driver)

    def parse_link_data(self, link_elements):
        """Parse and return the URL and filename of each document link provided.

        Args:
            link_elements ([WebElement]): List of link elements to parse.

        Returns:
            [dict]: List of dictionaries containing the URL and filename from each link element.
        """
        self.documents.wait_for_loaded()
        hrefs = []
        for link in link_elements:
            url = link.get_attribute('href')
            filename = link.text.strip()
            hrefs.append({
                'url': url,
                'filename': filename,
            })
        return hrefs

    def collect_folder_doc_urls(self, section_element):
        """Collect and return the URL and filename of each document link in a documents section.

        Args:
            section_element (WebElement): Target section div of the documents section.

        Returns:
            [dict]: List of dictionaries containing the URL and filename from each link element in the section.
        """
        link_data = []
        # expand the folders
        for folder in section_element.find_elements(*Locators.FOLDER):
            folder.find_element(*Locators.FOLDER_TOGGLE).click()
            self.documents.wait_for_loaded()
            link_data.extend(self.parse_link_data(folder.find_elements(*Locators.DOCUMENT_LINK)))

            if len(folder.find_elements(*Locators.PAGY)) > 0:
                next_link = folder.find_element(*Locators.PAGY).find_element(By.CLASS_NAME, 'page.next')
                while 'disabled' not in next_link.get_attribute('class'):
                    folder.find_element(*Locators.PAGY).find_element(By.CLASS_NAME, 'page.next').click()
                    self.documents.wait_for_loaded()
                    link_data.extend(self.parse_link_data(folder.find_elements(*Locators.DOCUMENT_LINK)))
                    next_link = folder.find_element(*Locators.PAGY).find_element(By.CLASS_NAME, 'page.next')

        return link_data

    def collect_all_document_urls(self):
        """Collect and return the URL and filename of all document links in the records request.

        Returns:
            [dict]: List of dictionaries containing the URL and filename from each link element in the request.
        """
        link_data = []

        for section in self.documents.doc_sections:
            section_element = self.documents.find_element(By.ID, section['id'])
            doc_links = section_element.find_elements(*Locators.DOCUMENT_LINK)
            folder_doc_links = self.collect_folder_doc_urls(section_element)

            bolds_count = len(section_element.find_elements(By.TAG_NAME, 'b'))
            if bolds_count > 0:
                total_count = section_element.find_elements(By.TAG_NAME, 'b')[bolds_count - 1].text
            else:
                total_count = 0
            print('Section contains a total of {} document links.'.format(total_count))

            link_data.extend(doc_links)
            link_data.extend(folder_doc_links)

            if len(section_element.find_elements(By.XPATH, '//*[@id="{}"]/nav'.format(section['id']))) == 1:
                def pagy():
                    """To avoid stale element errors, find the pagination element each time it's needed,
                        as opposed to storing the element.

                    Returns:
                        WebElement: Pagination element.
                    """
                    self.documents.wait_for_loaded()
                    return flaky_find(section_element, (By.XPATH, '//*[@id="{}"]/nav'.format(section['id'])))

                def current_page():
                    self.documents.wait_for_loaded()
                    self.documents.wait_for_loaded()
                    # _pagy = pagy()
                    # actives = _pagy.find_elements(*Locators.PAGY_ACTIVE)
                    # if len(actives) < 1:
                    #     polling.poll(
                    #         lambda: len(pagy().find_elements(*Locators.PAGY_ACTIVE)) > 0,
                    #         step=WAIT_INTERVAL,
                    #         timeout=LONG_WAIT_TIME,
                    #     )
                    return flaky_find(pagy(), Locators.PAGY_ACTIVE)

                def next_page():
                    self.documents.wait_for_loaded()
                    return flaky_find(pagy(), (By.LINK_TEXT, str(int(current_page().text) + 1)))

                def wait_for_page_active(page_number):
                    """Wait until the next page is active.

                    Returns:
                        bool: True if next page is active.
                    """
                    self.documents.wait_for_loaded()
                    polling.poll(
                        lambda: page_number in current_page().text,
                        step=WAIT_INTERVAL,
                        timeout=LONG_WAIT_TIME,
                    )
                    return True

                while len(pagy().find_elements(*Locators.PAGY_NEXT)) == 1 and 'disabled' not in pagy().find_element(
                        *Locators.PAGY_NEXT).get_attribute('class'):
                    start_count = len(link_data)
                    start_page = current_page().text
                    print_pagy(pagy())
                    if 'disabled' not in pagy().find_element(*Locators.PAGY_NEXT).get_attribute('class'):
                        print('Navigating to page {}...'.format(next_page().text))
                        self.documents.wait_for_loaded()
                        wait_for_page_active(current_page().text)

                        next_link = flaky_find(pagy(), Locators.PAGY_NEXT)
                        next_link.click()

                        self.documents.wait_for_loaded()
                        wait_for_page_active(str(int(start_page) + 1))

                        link_data.extend(self.parse_link_data(section_element.find_elements(*Locators.DOCUMENT_LINK)))
                        link_data.extend(self.collect_folder_doc_urls(section_element))

                        print('Collected {} new document links. Total: {} of {}'.format(
                            str(len(link_data) - start_count), len(link_data), total_count))

        return link_data
