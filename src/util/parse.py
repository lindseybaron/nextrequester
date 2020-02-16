import math
import re

from bs4 import BeautifulSoup as bs

from util.constants import BASE_URL, DOCUMENTS_FOLDER_URL, DOCUMENTS_SECTION_URL, DOCUMENTS_FOLDER_PAGE_URL, \
    DOCUMENTS_SECTION_PAGE_URL


def parse_doc_link(link, num_, collection, sub_dir=''):
    return {
        'url': '{}{}'.format(BASE_URL, link['href']),
        'filename': link.text,
        'num': len(collection) + num_,
        'sub_dir': sub_dir,
    }


def parse_request_id(session, user_req_id):
    print('User request ID: {}'.format(user_req_id))
    request_response = session.get('{}/requests/{}'.format(BASE_URL, user_req_id))
    request_content = request_response.content

    request_id = re.search('request_id: "([0-9]+?)"', str(request_content)).group(1)
    print('Other request ID: {}'.format(request_id))

    return request_id


def parse_folder_label(folder):
    return folder.parent.find(class_='font-size-14').text.replace(' ', '+')


def parse_section_page_count(section):
    section_pagination = section.find(class_='pagination')
    section_total = int(section_pagination.next_sibling.next_sibling.next_sibling.next_sibling.text)
    return math.ceil(section_total / 50)


def parse_folder_page_count(folder):
    folder_pagination = folder.find(class_='pagination')
    folder_total = int(folder_pagination.next_sibling.next_sibling.next_sibling.next_sibling.text)
    return math.ceil(folder_total / 20)


# There are two sections of responsive file attachments visible to user: public and requester.
# Public files are (obvs) public, and requester files are only visible to the requester.
# The HTML for each section is nested in JS in the response, and has to be parsed out.
def extract_documents_section_html(text, state):
    lines = text.split('\n')
    for l in lines:
        if '{}-docs'.format(state) in l:
            return l.replace('$("#{}-docs").html("'.format(state), '').replace('");', '').replace('\\\'',
                                                                                                   '\'').replace(
                '\\n', '').replace('\\"', '"').replace('  ', '').replace('<\\/', '</')


def extract_documents_folder_html(text, state, folder_label):
    lines = text.split('\n')
    folder_name = folder_label.replace('+', '').replace('-', '')
    for l in lines:
        if 'html' in l:
            return l.replace('$(".state-{}.folder-{}").html("'.format(state, folder_name), '').replace(
                '");', '').replace('\\\'', '\'').replace('\\n', '').replace('\\"', '"').replace(
                '  ', '').replace('<\\/', '</')


def fetch_section_soup(session, request_id, state):
    section_url = DOCUMENTS_SECTION_URL.format(BASE_URL, request_id, state)
    print('Fetching {}...'.format(section_url))
    docs_response = session.get(section_url)
    html = extract_documents_section_html(text=docs_response.text, state=state)
    return bs(html, 'html.parser')


def fetch_section_page_soup(session, state, request_id, page_num):
    section_page_url = DOCUMENTS_SECTION_PAGE_URL.format(BASE_URL, request_id, state, page_num)
    print('Fetching {}...'.format(section_page_url))
    section_page_response = session.get(section_page_url)
    section_page_html = extract_documents_section_html(text=section_page_response.text, state=state)
    return bs(section_page_html, 'html.parser')


def fetch_folder_soup(session, label, state, request_id):
    folder_url = DOCUMENTS_FOLDER_URL.format(BASE_URL, label, state, request_id)
    print('Fetching {}...'.format(folder_url))
    folder_response = session.get(folder_url)
    folder_html = extract_documents_folder_html(text=folder_response.text, state=state, folder_label=label)
    return bs(folder_html, 'html.parser')


def fetch_folder_page_soup(session, label, state, request_id, page_num):
    folder_page_url = DOCUMENTS_FOLDER_PAGE_URL.format(BASE_URL, label, state, request_id, page_num)
    print('Fetching {}...'.format(folder_page_url))
    folder_page_response = session.get(folder_page_url)
    folder_page_html = extract_documents_folder_html(text=folder_page_response.text, state=state, folder_label=label)
    return bs(folder_page_html, 'html.parser')
