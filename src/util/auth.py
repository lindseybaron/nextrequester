import urllib.parse

from bs4 import BeautifulSoup as bs

from util.constants import LOGIN_URL

initial_headers = {
    'User-Agent': ' '.join([
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36',
        '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'])
}
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


def login_driver(driver, user):
    driver.delete_all_cookies()

    _login_response = driver.request('GET', LOGIN_URL, headers=initial_headers)
    _login_soup = bs(_login_response.content, 'html.parser')
    _token = _login_soup.find(attrs={"name": "csrf-token"})['content']
    token = urllib.parse.quote_plus(_token)
    login_params = build_login_params(token=token, email=user['email'], pw=user['pw'])
    driver.request('POST', LOGIN_URL, headers=sign_in_headers, params=login_params)


def login_session(session, user):
    session.cookies.clear()
    _login_response = session.request('GET', LOGIN_URL, headers=initial_headers)
    _login_soup = bs(_login_response.content, 'html.parser')
    _token = _login_soup.find(attrs={"name": "csrf-token"})['content']
    token = urllib.parse.quote_plus(_token)
    login_params = build_login_params(token=token, email=user['email'], pw=user['pw'])
    session.request('POST', LOGIN_URL, headers=sign_in_headers, params=login_params)


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
