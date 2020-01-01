import os

import yaml
from selenium import webdriver

from util.constants import CONFIG_PATH, BIN_DIR, ROOT_DIR


def parse_config():
    with open(CONFIG_PATH) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def parse_secret():
    secret_path = os.path.abspath(os.path.join(ROOT_DIR, 'secret.yaml'))

    if os.path.exists(secret_path):
        with open(secret_path) as file:
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


def get_download_dir():
    config = parse_config()
    download_dir_path = config.get('download_dir', '')

    if download_dir_path:
        print('Attempting to use download directory {}...'.format(download_dir_path))
        download_dir = os.path.abspath(download_dir_path)
        # if download_dir is valid, use that
        if os.path.exists(download_dir):
            print('Found {}.'.format(download_dir_path))
            return download_dir_path
        else:
            # if download_dir doesn't exist, try to create it
            print('Could not find {}. Attempting to create it...'.format(download_dir_path))
            try:
                os.mkdir(download_dir)
                print('Created {}.'.format(download_dir_path))
                return download_dir_path
            except FileExistsError as e:
                print(e)
    else:
        print('No download directory specified. Using default Chrome download directory (probably ~/Downloads).')
        return


def get_driver(request_id=None):
    options = webdriver.ChromeOptions()

    # set download directory
    download_dir = get_download_dir()
    if download_dir and request_id:
        download_dir = os.path.join(download_dir, request_id)
    # if download_dir isn't set in config, use default
    if download_dir:
        print('Downloading files to {}.'.format(download_dir))
        options.add_argument("download.default_directory={}".format(download_dir))

    # set binary path
    binary_path = get_binary_path()

    return webdriver.Chrome(binary_path, options=options)
