import os

# files and directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../..'))
CONFIG_PATH = os.path.abspath(os.path.join(ROOT_DIR, 'config.yaml'))
DATA_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'data'))
BIN_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'bin'))

CHROME_PATH = os.path.abspath(os.path.join(ROOT_DIR, 'bin/chromedriver'))

# urls
BASE_URL = "https://lacity.nextrequest.com"
REQUEST_URL = BASE_URL + "/requests/{request_id}"
LOGIN_URL = BASE_URL + "/users/sign_in"

# browser
SELENIUM_WAIT_TIME = 10
SELENIUM_SLEEP_INTERVAL = 0.5
