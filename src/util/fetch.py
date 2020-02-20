import asyncio
import math
import os
from pathlib import Path

import aiofiles as aiofiles
import aiohttp
from aiohttp import ClientResponseError, ClientConnectionError
from bs4 import BeautifulSoup as bs

from util.config import get_download_dir
from util.constants import DEFAULT_HEADERS, REQUESTS_URL, BASE_URL
from util.parse import parse_request_row


async def afetch(session, url):
    async with session.get(url) as response:
        print('fetching {}...'.format(url))
        text = await response.text()

        return {'text': text, 'url': url}


async def adownload_file(url, filename, headers, cookies, sub_dir=None, msg=None):

    # prepare path
    if sub_dir:
        dl_dir = os.path.join(get_download_dir(), sub_dir)
        # if directory doesn't exist, create it
        Path(dl_dir).mkdir(parents=True, exist_ok=True)
    else:
        dl_dir = get_download_dir()
        # if directory doesn't exist, create it
        Path(dl_dir).mkdir(parents=True, exist_ok=True)
    dl_path = os.path.join(dl_dir, filename.replace('/', '-').replace(':', '-').replace(' ', '_'))

    # write file
    _headers = headers.update(DEFAULT_HEADERS)
    connector = aiohttp.TCPConnector(limit=40)
    # timeout = aiohttp.ClientTimeout(total=120)
    async with aiohttp.ClientSession(
            connector=connector,
            headers=_headers,
            cookies=cookies,
            # timeout=timeout
    ) as client:
        print('Fetching file {} from {}...'.format(filename, url))
        async with client.get(url) as resp:
            try:
                resp.raise_for_status()
            except ClientResponseError as e:
                print('Failed to download {} from {}.\n{}'.format(filename, url, e))

            try:
                f = await aiofiles.open(dl_path, 'wb')
                await f.write(await resp.read())
                print('{} Saved {} to {}...'.format(msg, url, dl_path))
                await asyncio.sleep(5)
            except ClientConnectionError as e:
                print('Failed to save {} from {}.\n{}'.format(filename, url, e))
            finally:
                await f.close()
                await client.close()


async def gather_all_requests(session):

    requests = []

    # fetch the first page of the documents list to calculate the number of pages.
    count_response = session.get(REQUESTS_URL)
    soup = bs(count_response.content, 'html.parser')

    # get the total number of results...
    results_count = int(soup.find(class_='count').text)
    # and calculate number of pages based on number shown per page (25 by default).
    # for some reason, passing the per_page param doesn't work on /requests like it does on /documents
    per_page = 25  # TODO: figure out a way to do 100 per page
    page_count = math.ceil(results_count / per_page)
    # build a list of urls from the page numbers and other parameters
    page_param = ['requests_smart_listing[page]={}'.format(p) for p in range(1, page_count + 1)]
    list_page_urls = ['{}/requests?{}'.format(BASE_URL, pp) for pp in page_param]

    # use asession to asynchronously fetch each of the urls in the list
    asession = aiohttp.ClientSession(
        headers=session.headers,
        cookies=session.cookies,
    )

    async with asession:
        # fetch each page of the requests list
        list_page_responses = await asyncio.gather(*[afetch(asession, u) for u in list_page_urls])

    for list_page_response in list_page_responses:
        soup = bs(list_page_response['text'], 'html.parser')
        rows = soup.find_all(class_='demo-data-false')
        for row in rows:
            requests.append(parse_request_row(row))

    return requests


async def fetch_request_pages(session, request_data, batch_size=50):

    pages = []

    # split request data into batches
    batches = batch_data(data=request_data, batch_size=batch_size)
    request_responses = []

    for batch in batches:

        async with aiohttp.ClientSession(
            headers=session.headers,
            cookies=session.cookies,
        ) as asession:
            # fetch each page of the requests list
            responses = await asyncio.gather(*[afetch(asession, r['url']) for r in batch])
            request_responses.extend(responses)

    for p in request_responses:
        pages.append(bs(p['text'], 'html.parser'))

    return pages


def batch_data(data, batch_size):
    _range = range((len(data) + batch_size - 1) // batch_size)
    return [data[i * batch_size:(i + 1) * batch_size] for i in _range]
