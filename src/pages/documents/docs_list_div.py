import asyncio
import re
from concurrent.futures.thread import ThreadPoolExecutor
from timeit import default_timer

from bs4 import BeautifulSoup as bs

from pages.documents.locators import DocumentsLocators as Locators
from pages.element import Element
from util.constants import BASE_URL
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
                'url': doc_url,
                'filename': filename,
            })

        return results

    async def gather_result_links(self, nums, per_page=100):
        # static params
        per_page_param = 'documents_smart_listing[per_page]={}'.format(per_page)
        sort_param = 'documents_smart_listing[sort][count]=desc'
        params = '&'.join([per_page_param, sort_param])
        # page param
        page_params = ['documents_smart_listing[page]={}'.format(p) for p in range(start=1, stop=nums + 1)]
        urls = ['{}/documents?{}&{}'.format(BASE_URL, pp, params) for pp in page_params]

        # range_ = range(1, per_page + 1)
        # for i in range_:
        #     yield i
        #     await asyncio.sleep(0)

        for url in urls:
            response = self.driver.request('GET', url)
            soup = bs(response.content, 'html.parser')
            rows = soup.find_all(class_=Locators.LIST_ROW[1])
            results = [{'url': r.get_attribute('href') } for r in rows]

            yield results
            await asyncio.sleep(0)

    def fetch_results(self, url, start_time):
        with self.driver.request('GET', url) as response:
            if response.status_code != 200:
                print("FAILURE::{0}".format(url))
            else:
                soup = bs(response.content, 'html.parser')
                _list = soup.find(class_='documents')
                _rows = _list.find(class_=Locators.LIST_ROW[1])
            elapsed = default_timer() - start_time
            time_completed_at = "{:5.2f}s".format(elapsed)
            print("{0:<30}\t\t\t\t\t\t\t\t{1:>20}".format(url, time_completed_at))

            return response

    async def async_fetch_page_results(self, urls):
        print("{0:<30}\t\t\t\t\t\t\t\t{1:>20}".format("URL", "Completed at"))

        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()

            start_time = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    self.fetch_results,
                    *(self.driver, url, start_time)
                )
                for url in urls
            ]

            for response in await asyncio.gather(*tasks):
                pass
