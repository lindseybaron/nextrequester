import os

from util.config import get_download_dir


def file_exists(link, sub_dir=None):
    filename = link.text
    dl_dir = os.path.join(get_download_dir(), sub_dir if sub_dir else get_download_dir())
    path = os.path.join(dl_dir, filename)
    if os.path.exists(path):
        print('File {} already exists at {}.'.format(filename, path))
        # TODO: binary compare files to prevent duplicate downloads

    return True


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
            _filename.replace('.{}'.format(ext), ''),
            parse_document_id(url),
            ext,
        )
