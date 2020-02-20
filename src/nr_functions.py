import asyncio
import datetime
import math
import os
import re

import aiohttp
from bs4 import BeautifulSoup as bs

from util.auth import login
from util.constants import DOCUMENTS_SECTIONS, DOCUMENTS_URL, BASE_URL, DATA_DIR
from util.fetch import adownload_file, afetch, gather_all_requests, fetch_request_pages, batch_data
from util.file import build_filename, parse_document_id
from util.parse import (
    parse_request_id, fetch_section_soup, parse_doc_link, parse_folder_label, fetch_folder_soup,
    parse_folder_page_count, fetch_folder_page_soup, parse_section_page_count, fetch_section_page_soup
)


async def download_all_request_files(req_id, email=None, pw=None):
    # log in
    rsession = login(email=email, pw=pw)

    # get the "request id", which is different from the one in the URL for some stupid reason
    request_id = parse_request_id(rsession, req_id)

    doc_links = []
    for state in DOCUMENTS_SECTIONS:
        # fetch the section
        section_soup = fetch_section_soup(rsession, request_id, state)
        section_links = []

        # collect section-level document links on first page
        section_first_page_links = []
        s_num = 1
        for sfp_link in section_soup.find_all(class_='document-link'):
            section_first_page_links.append(parse_doc_link(sfp_link, s_num, doc_links))
            s_num = s_num + 1
        # and add them to the main collection
        print('Adding {} document links to collection.'.format(len(section_first_page_links)))
        section_links.extend(section_first_page_links)

        # collect folders, if any
        document_folders = section_soup.find_all(class_='fa-folder')
        # if there are folders, we need the labels to fetch the folder content
        folder_labels = []
        for folder in document_folders:
            folder_labels.append(parse_folder_label(folder))

        # use the folder labels to fetch content of each folder
        for label in folder_labels:
            folder_soup = fetch_folder_soup(rsession, label, state, request_id)

            # collect folder-level document links on first page of folder
            folder_first_page_links = []
            ffp_num = 1
            for ffp_link in folder_soup.find_all(class_='document-link'):
                folder_first_page_links.append(parse_doc_link(ffp_link, ffp_num, doc_links, sub_dir=label))
                ffp_num = ffp_num + 1
            # and add them to the main collection
            print('Adding {} document links to collection.'.format(len(folder_first_page_links)))
            section_links.extend(folder_first_page_links)

            # check for additional folder-level pages
            if folder_soup.find_all(class_='pagination'):
                # determine how many pages there are in the folder
                folder_page_count = parse_folder_page_count(folder_soup)
                # collect document links from each folder page
                for fp_page in range(2, folder_page_count + 1):
                    # fetch the folder page
                    folder_page_soup = fetch_folder_page_soup(rsession, label, state, request_id, fp_page)

                    # collect folder-level document links on the folder page
                    folder_page_links = []
                    fp_num = 1
                    for fp_link in folder_page_soup.find_all(class_='document-link'):
                        folder_page_links.append(parse_doc_link(fp_link, fp_num, doc_links, sub_dir=label))
                        fp_num = fp_num + 1
                    # and add them to the main collection
                    print('Adding {} document links to collection.'.format(len(folder_page_links)))
                    section_links.extend(folder_page_links)

        # check for additional section-level pages
        if section_soup.find_all(class_='pagination'):
            # determine how many pages there are in the section
            section_page_count = parse_section_page_count(section_soup)
            # collect document links from each section page
            for s_page in range(2, section_page_count + 1):
                # fetch section page
                section_page_soup = fetch_section_page_soup(rsession, state, request_id, s_page)

                # collect section-level document links on section page
                section_page_links = []
                sp_num = 1
                for sp_link in section_page_soup.find_all(class_='document-link'):
                    links = parse_doc_link(sp_link, sp_num, doc_links)
                    section_page_links.append(links)
                    sp_num = sp_num + 1
                # and add them to the main collection
                print('Adding {} document links to collection.'.format(len(section_page_links)))
                section_links.extend(section_page_links)

        doc_links.extend(section_links)

    link_filename = '{}_links.txt'.format(req_id)
    link_file_path = os.path.abspath(os.path.join(DATA_DIR, link_filename))
    with open(link_file_path, 'w') as file:
        for l in doc_links:
            file.write(l['url'] + '\n')

    batches = batch_data(data=doc_links, batch_size=20)
    for batch in batches:
        await asyncio.gather(
            *[adownload_file(
                url=d['url'],
                filename=d['filename'],
                headers=rsession.headers,
                cookies=rsession.cookies,
                sub_dir='{}/{}'.format(req_id, d['sub_dir']),
                msg='',
            ) for d in batch])

    rsession.close()


async def download_all_documents(email=None, pw=None):
    """Download all the files found at /documents. Can be run without auth, but will only include
    all files with auth.

    Args:
        email (str):
        pw (str):
    """
    rsession = login(email, pw)

    # fetch the first page of the documents list to calculate the number of pages.
    count_response = rsession.get('{}?documents_smart_listing[per_page]=100'.format(DOCUMENTS_URL))

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
        num = 1

        for doc_page_response in doc_page_responses:
            doc_page = bs(doc_page_response['text'], 'html.parser')
            page_header = doc_page.find(class_='document-header')

            if page_header:
                filename = build_filename(page_header, doc_page_response['url'])
            else:
                filename = 'missing filename {}'.format(parse_document_id(doc_page_response['url']))

            if not filename:
                print('failed to parse filename for file at {}'.format(doc_page_response['url']))
            dl_data.append({
                'filename': filename,
                'url': doc_page_response['url'],
                'num': num,
            })
            num = num + 1
        total = len(dl_data)

        # download each file and save it to the appropriate location
        await asyncio.gather(
            *[adownload_file(
                headers=rsession.headers,
                cookies=rsession.cookies,
                url=d['url'],
                filename=d['filename'],
                sub_dir='documents',
                msg='{}/{}'.format(d['num'], total),
            ) for d in dl_data if d['url']])


async def print_all_requests(email=None, pw=None, outfile='requests.csv'):
    rsession = login(email, pw)

    requests_data = await gather_all_requests(session=rsession)

    for req in requests_data:
        line = '{url}\t{id}\t{status}\t{date}\t"{desc}"\t"{depts}"\t"{pocs}"'.format(
            url=req['url'],
            id=req['id'],
            status=req['status'],
            date=req['date'],
            desc=req['desc'],
            depts=req['depts'],
            pocs=req['pocs'],
        )

        print(line, file=open(outfile, 'a'))


async def print_my_requests(email=None, pw=None, outfile=None):

    my_requests = []

    # log in
    rsession = login(email=email, pw=pw)

    # gather urls for all requests
    requests_data = await gather_all_requests(session=rsession)

    # fetch each request page
    request_pages = await fetch_request_pages(session=rsession, request_data=requests_data)
    for req in request_pages:
        # if it has the envelope, add it to the collection
        if req.find_all(class_='qa-envelope'):
            r_id = re.search('Request ([0-9]{2}-[0-9]+) -', str(req.title)).group(1)
            my_requests.append({
                'url': '{}/requests/{}'.format(BASE_URL, r_id),
                'id': r_id,
                'status': req.find(class_='request-state').text.strip(),
                'date': datetime.datetime.strptime(
                    req.find(class_='request_date').find('strong').text.strip(),
                    '%B %d, %Y'
                ),
                'desc': req.find(class_='request-text').text.strip(),
                'depts': req.find(class_='current-department').text.strip(),
                'pocs': req.find(class_='request-detail').text.strip(),
                'requester': req.find(class_='requester-details').find(class_='fa-envelope').next_sibling.strip(),
            })

    # sort collection by request date
    sorted(my_requests, key=lambda i: i['date'])
    # print collection to console and file
    out_path = os.path.abspath(os.path.join(DATA_DIR, outfile))
    url_list_path = os.path.abspath(os.path.join(DATA_DIR, 'my_request_urls.txt'))
    with open(out_path, 'w') as file:
        for req in my_requests:
            line = '{url}\t{id}\t{status}\t{date}\t"{desc}"\t"{depts}"\t"{pocs}"\n'.format(
                url=req['url'],
                id=req['id'],
                status=req['status'],
                date=req['date'],
                desc=req['desc'],
                depts=req['depts'],
                pocs=req['pocs'],
            )
            file.write(line)

            print(req['url'] + '\n', file=open(url_list_path, 'a'))
