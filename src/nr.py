import asyncio

import fire
import requests

from pages.documents.documents_page import DocumentsPage
from pages.login.login_page import LoginPage
from pages.records_request.request_page import RecordRequestPage
from util.auth import login
from util.config import load_user
from util.driver import get_driver
from util.fetch import download_all_documents


class NextRequest(object):

    @staticmethod
    def batch(req, user=None, pw=None):

        user = load_user(user, pw)

        driver = get_driver(sub_dir=req)
        LoginPage(driver).login(user['email'], user['pw'])

        request_page = RecordRequestPage(driver, request_id=req)
        request_page.visit()
        request_page.download_all_files()

    @staticmethod
    def alldocs(user=None, pw=None):
        rsession = requests.Session()
        login(rsession, load_user(email=user, pw=pw))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_documents(rsession=rsession))


if __name__ == '__main__':
    NextRequest.alldocs()
    # next_requester = NextRequest()
    # fire.Fire(next_requester)
