import os

from selenium import webdriver
from seleniumrequests import Chrome

from util.config import parse_config, get_platform, get_download_dir
from util.constants import BIN_DIR


def get_binary_path():
    config = parse_config()
    platform = config.get('platform', get_platform())
    print('Running on {}.'.format(platform))
    version = config.get('chrome_version', '79')
    print('Using Chrome version {}'.format(version))

    path = os.path.abspath(os.path.join(BIN_DIR, platform, str(version), 'chromedriver'))
    print('located at {}.'.format(path))

    return path


def get_driver(sub_dir=None):
    options = webdriver.ChromeOptions()

    # set download directory
    download_dir = get_download_dir()
    if download_dir and sub_dir:
        download_dir = os.path.join(download_dir, sub_dir)
    # if download_dir isn't set in config, use default
    if download_dir:
        print('Downloading files to {}.'.format(download_dir))
        prefs = {'download.default_directory': download_dir}
        options.add_experimental_option('prefs', prefs)

    # set binary path
    binary_path = get_binary_path()

    driver = Chrome(binary_path, options=options)
    driver.maximize_window()

    return driver
