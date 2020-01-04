import asyncio
import math
import os

import aiohttp
from bs4 import BeautifulSoup as bs

from util.constants import DOCUMENTS_URL, BASE_URL
from util.file import get_download_dir, build_filename, parse_document_id


async def afetch(session, url):
    async with session.get(url) as response:
        print('fetching {}...'.format(url))
        text = await response.text()

        return {
            'text': text,
            'url': url,
        }


async def adownload_file(session, url, filename):
    # fetch file
    async with session.get(url) as response:
        dl_dir = os.path.join(get_download_dir(), 'documents')
        dl_path = os.path.join(dl_dir, filename.replace('/', '-').replace(':', '-'))
        print('Downloading {} to {}...'.format(url, dl_path))
        # write file
        _file = await response.read()
        with open(dl_path, 'wb') as file:
            file.write(_file)

        return filename


async def download_all_documents(rsession):
    """Download all the files found at /documents. Can be run without auth, but will only include
    all files with auth.

    :param rsession: requests.Session() instance (with or without authentication).
        Note: This session is used for synchronous functionality, whereas asession is used for
            asynchronous functionality. Cookies and headers are copied from rsession to asession.
    """
    # fetch the first page of the documents list to calculate the number of pages.
    count_response = rsession.get(DOCUMENTS_URL + '?documents_smart_listing[per_page]=100')

    # get the total number of results...
    results_count = int(bs(count_response.content, 'html.parser').find(class_='count').text)
    # and calculate number of pages when 100 results are shown per page.
    page_count = math.ceil(results_count / 100)
    # build a list of urls from the page numbers and other parameters
    per_page_param = 'documents_smart_listing[per_page]={}'.format(100)
    sort_param = 'documents_smart_listing[sort][count]=desc'
    params = '&'.join([per_page_param, sort_param])
    page_params = ['documents_smart_listing[page]={}'.format(p) for p in range(1, page_count + 1)]
    list_page_urls = ['{}/documents?{}&{}'.format(BASE_URL, pp, params) for pp in page_params]

    # use asession to asynchronously fetch each of the urls in the list
    asession = aiohttp.ClientSession(
        headers=rsession.headers,
        cookies=rsession.cookies,
    )
    dl_data = []

    async with asession:
        # fetch each page of the documents list
        list_page_responses = await asyncio.gather(*[afetch(asession, u) for u in list_page_urls])
        doc_page_urls = set()

        for list_page_response in list_page_responses:
            response_text = list_page_response['text']
            soup = bs(response_text, 'html.parser')
            doc_links = soup.find_all(class_='document published')
            print('found {} links on page.'.format(len(doc_links)))
            doc_page_urls.update(['{}{}'.format(BASE_URL, link['href']) for link in doc_links])

        # fetch each of the document pages to get the full filename (since the list tends to cut them off)
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

        # download each file and save it to the appropriate location
        await asyncio.gather(
            *[adownload_file(asession, d['url'], d['filename']) for d in dl_data if d['url']]
        )
