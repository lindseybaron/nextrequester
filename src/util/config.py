import os

import yaml

from util.constants import CONFIG_PATH, ROOT_DIR, DATA_DIR

MISSING_EMAIL_MSG = ('No email address provided for login. ',
                     'Pass via command line with --email=XXXXX or set in secret.yaml in project root directory')
INVALID_EMAIL_MSG = ('Email address in secret.yaml is invalid. '
                     'Enter a valid email address, or remove it and pass via command line with `--email=XXXXX`.')
MISSING_PW_MSG = ('No password provided for login. ',
                  'Pass via command line with --pw=XXXXX or set in secret.yaml in project root directory')
INVALID_PW_MSG = ('Password in secret.yaml is invalid.',
                  'Enter a valid password, or remove it and pass via command line with --pw=XXXXX')


def validate_email(email):
    if email and len(email) > 1 and '@' in email:
        return email
    else:
        raise ValueError(INVALID_EMAIL_MSG)


def validate_pw(pw):
    if pw and len(pw) > 1:
        return pw
    else:
        raise ValueError(INVALID_PW_MSG)


def get_secret(key):
    value = parse_secret()[key]
    if 'email' in key:
        if value:
            return validate_email(value)
    elif 'pw' in key:
        if value:
            return validate_pw(value)
    else:
        raise ValueError('Invalid key.')


def load_user(email=None, pw=None):
    if not email:
        email = get_secret('email')
    if not pw:
        pw = get_secret('pw')

    # make sure email and pw are set before proceeding
    assert email, MISSING_EMAIL_MSG
    assert pw, MISSING_PW_MSG

    return {
        'email': email,
        'pw': pw
    }


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


def get_download_dir():
    config = parse_config()
    secret = parse_secret()
    if 'download_dir' in config.keys():
        download_dir_path = config['download_dir']
    elif 'download_dir' in secret.keys():
        download_dir_path = secret['download_dir']
    else:
        download_dir_path = DATA_DIR

    download_dir = os.path.abspath(download_dir_path)
    # if download_dir is valid, use that
    if os.path.exists(download_dir):
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
