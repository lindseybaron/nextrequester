import os

# files and directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../..'))
CONFIG_PATH = os.path.abspath(os.path.join(ROOT_DIR, 'config.yaml'))
DATA_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'data'))

# urls
BASE_URL = 'https://lacity.nextrequest.com'
LOGIN_URL = BASE_URL + '/users/sign_in'
REQUESTS_URL = BASE_URL + '/requests'
DOCUMENTS_URL = BASE_URL + '/documents'

# request documents
DOCUMENTS_SECTIONS = ['requester', 'public']
DOCUMENTS_SECTION_URL = '{}/documents/batch?request_id={}&state={}&_=1581458452674'
DOCUMENTS_SECTION_PAGE_URL = '{}/documents/batch?request_id={}&state={}&_=1581458452674&page={}'
DOCUMENTS_FOLDER_URL = '{}/documents/documents_by_folder?folder={}&state={}&request_id={}&subfolder='
DOCUMENTS_FOLDER_PAGE_URL = '{}/documents/documents_by_folder?folder={}&state={}&request_id={}&subfolder=&page={}'

DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'x-requested-with': 'XMLHttpRequest',
    'Connection': 'close',
}
