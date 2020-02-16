import urllib.parse

import requests
from bs4 import BeautifulSoup as bs

from util.config import load_user
from util.constants import LOGIN_URL, BASE_URL, DEFAULT_HEADERS

sign_in_headers = {
    'authority': 'lacity.nextrequest.com',
    'method': 'POST',
    'path': '/users/sign_in',
    'scheme': 'https',
    'accept': 'text/html, application/xhtml + xml, application/xml',
    'upgrade-insecure-requests': '1',
    'user-agent': ' '.join([
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'])
}


def login(email, pw):

    print('Logging in...')

    user = load_user(email, pw)
    session = requests.session()
    session.cookies.clear()

    response = session.request('GET', LOGIN_URL, headers=DEFAULT_HEADERS)
    soup = bs(response.content, 'html.parser')
    token = urllib.parse.quote_plus(soup.find(attrs={"name": "csrf-token"})['content'])
    login_params = build_login_params(token=token, email=user['email'], pw=user['pw'])
    session.request('POST', LOGIN_URL, headers=sign_in_headers, params=login_params)
    session.headers.update({'x-requested-with': 'XMLHttpRequest'})

    return session


def build_login_params(token, email, pw):
    return '&'.join([
        'utf8=✓',
        'authenticity_token={}'.format(token),
        'user[email]={}'.format(email),
        'user[password]={}'.format(pw),
        'user[remember_me]=0',
        'user[remember_me]=1',
        'button=',
    ])


def get_csrf_token(session):
    response = session.get(BASE_URL)
    soup = bs(response.content)

    return soup.find(attrs={"name": "csrf-token"})['content']
