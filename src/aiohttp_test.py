import asyncio
import math

import aiohttp
import requests
from bs4 import BeautifulSoup as bs

from util.config import load_user
from util.constants import DOCUMENTS_URL, BASE_URL
from util.fetch import afetch, adownload_file
from util.file import build_filename, parse_document_id
from util.auth import login


async def main():
    rsession = requests.Session()
    login(rsession, load_user(None, None))
    count_response = rsession.get(DOCUMENTS_URL + '?documents_smart_listing[per_page]=100')

    results_count = int(bs(count_response.content, 'html.parser').find(class_='count').text)
    page_count = math.ceil(results_count / 100)
    per_page_param = 'documents_smart_listing[per_page]={}'.format(100)
    sort_param = 'documents_smart_listing[sort][count]=desc'
    params = '&'.join([per_page_param, sort_param])
    # page param
    page_params = ['documents_smart_listing[page]={}'.format(p) for p in range(1, page_count + 1)]
    list_page_urls = ['{}/documents?{}&{}'.format(BASE_URL, pp, params) for pp in page_params]

    asession = aiohttp.ClientSession(
        headers=rsession.headers,
        cookies=rsession.cookies,
    )

    dl_data = []

    async with asession:
        list_page_responses = await asyncio.gather(*[afetch(asession, u) for u in list_page_urls])
        doc_page_urls = set()

        for list_page_response in list_page_responses:
            response_text = list_page_response['text']
            soup = bs(response_text, 'html.parser')
            doc_links = soup.find_all(class_='document published')
            print('found {} links on page.'.format(len(doc_links)))
            doc_page_urls.update(['{}{}'.format(BASE_URL, link['href']) for link in doc_links])

        doc_page_responses = await asyncio.gather(*[afetch(asession, d) for d in doc_page_urls])
        for doc_page_response in doc_page_responses:
            doc_page = bs(doc_page_response['text'], 'html.parser')
            page_header = doc_page.find(class_='document-header')
            if page_header:
                filename = build_filename(page_header, doc_page_response['url'])
            else:
                filename = 'missing filename {}'.format(parse_document_id(doc_page_response['url']))

            if not filename:
                print('failed to parse filename for file at {}'.format(doc_page_response['url']))
            data = {
                'filename': filename,
                'url': doc_page_response['url'],
            }
            dl_data.append(data)

        await asyncio.gather(
            *[adownload_file(asession, d['url'], d['filename']) for d in dl_data if d['url']]
        )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
