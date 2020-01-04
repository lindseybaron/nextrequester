import os

from util.config import parse_config


def file_exists(link, sub_dir=None):
    filename = link.text
    dl_dir = os.path.join(get_download_dir(), sub_dir if sub_dir else get_download_dir())
    path = os.path.join(dl_dir, filename)
    if os.path.exists(path):
        print('File {} already exists at {}.'.format(filename, path))
        # TODO: binary compare files to prevent duplicate downloads

    return True


def get_download_dir():
    config = parse_config()
    download_dir_path = config.get('download_dir', '')

    if download_dir_path:
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
    else:
        print('No download directory specified. Using default Chrome download directory (probably ~/Downloads).')
        return


def parse_document_id(url):
    url_parts = url.split('/')
    return url_parts[len(url_parts) - 1]


def parse_file_ext(filename):
    parts = filename.split('.')
    return parts[len(parts) - 1]


def build_filename(header_element, url):
    h3 = header_element.find('h3')
    if h3:
        h3_text = h3.text
        _filename = h3_text.strip().replace('/', '-').replace(':', '-').replace(' ', '_').replace('&', '-')
        ext = parse_file_ext(_filename)
        return '{} [{}].{}'.format(
            _filename.replace(ext, ''),
            parse_document_id(url),
            ext,
        )