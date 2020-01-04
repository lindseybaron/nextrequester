# import asyncio
# import math
#
# import aiohttp
# import requests
# from aiostream import stream, pipe
# from bs4 import BeautifulSoup as bs
# from requests import Request
#
# from pages.documents.locators import DocumentsLocators as Locators
# from util.constants import BASE_URL, LOGIN_URL, DOCUMENTS_URL
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# }
#
#
# async def fetch_doc_urls(urls):
#     xs = stream.iterate(urls) | pipe.map(fetch, ordered=True, task_limit=10)
#     async for result in xs:
#         soup = bs(str(result), 'html.parser')
#         rows = soup.find_all(class_=Locators.LIST_ROW[1])
#         _urls = [r.find(class_=Locators.ROW_DOC_LINK) for r in rows]
#         print(result)
#
#
# async def fetch(url):
#     print(url)
#     session = requests.Session()
#     response = session.request('GET', url)
#
#     return response.content
#
#
# async def main():
#     session = aiohttp.ClientSession()
#     session.cookies.clear()
#     _login_response = session.request('GET', LOGIN_URL, headers=headers)
#     _login_soup = bs(_login_response.content, 'html.parser')
#     token = _login_soup.find(attrs={"name": "csrf-token"})['content']
#     login_params = '&'.join([
#         'utf8=✓',
#         'authenticity_token={}'.format(token),
#         'user[email]=arasodhupana@foutu.org',
#         'user[password]=arasodhupana',
#         'user[remember_me]=0',
#         'user[remember_me]=1',
#         'button=',
#     ])
#     sign_in_headers = {
#         'authority': 'lacity.nextrequest.com',
#         'method': 'POST',
#         'path': '/users/sign_in',
#         'scheme': 'https',
#         'accept': 'text/html, application/xhtml + xml, application/xml',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
#     }
#     request = Request('POST', LOGIN_URL, headers=sign_in_headers, params=login_params)
#     prepared_req = session.prepare_request(request)
#
#     # response = session.request('POST', LOGIN_URL, params=login_params, headers=sign_in_headers)
#     response = session.send(prepared_req, verify=False, allow_redirects=True)
#
#     soup = bs(response.content, 'html.parser')
#     alert_bar_text = soup.find(class_='alert-bar').text
#     signed_in = 'signed in' in alert_bar_text
#
#     results_count = int(bs(
#         session.get(DOCUMENTS_URL + '?documents_smart_listing[per_page]=100').content,
#         'html.parser'
#     ).find(class_='count').text)
#     page_count = math.ceil(results_count / 100)
#     per_page_param = 'documents_smart_listing[per_page]={}'.format(100)
#     sort_param = 'documents_smart_listing[sort][count]=desc'
#     params = '&'.join([per_page_param, sort_param])
#     # page param
#     page_params = ['documents_smart_listing[page]={}'.format(p) for p in range(1, page_count + 1)]
#     urls = ['{}/documents?{}&{}'.format(BASE_URL, pp, params) for pp in page_params]
#
#     # results = await asyncio.gather(map(fetch_doc_urls, urls))
#     results = await fetch_doc_urls(urls)
#     print(results)
#
#
# if __name__ == "__main__":
#     import time
#
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")
