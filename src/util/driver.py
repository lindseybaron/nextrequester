import os
import yaml

from selenium import webdriver

from util.constants import DATA_DIR, CONFIG_PATH, BIN_DIR


def parse_config():
    with open(CONFIG_PATH) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def get_platform():
    platform = os.uname()
    if 'Darwin' in platform:
        return 'osx'
    elif 'Linux' in platform:
        return 'linux'


def get_binary_path():
    config = parse_config()
    platform = config.get('platform', get_platform())
    print('Running on {}.'.format(platform))
    version = config.get('chrome_version', '79')
    print('Using Chrome version {}'.format(version))

    path = os.path.abspath(os.path.join(BIN_DIR, platform, str(version), 'chromedriver'))
    print('located at {}.'.format(path))

    return path


def get_driver(request_id):
    options = webdriver.ChromeOptions()
    download_dir = os.path.abspath(os.path.join(DATA_DIR, request_id))
    print('Downloading files to {}.'.format(download_dir))
    options.add_argument("download.default_directory={}".format(download_dir))

    binary_path = get_binary_path()

    return webdriver.Chrome(binary_path, options=options)
