import asyncio

import fire
import requests

from util.auth import login_session
from util.config import load_user
from util.fetch import download_all_documents, download_all_request_files, print_all_requests


class NextRequest(object):

    @staticmethod
    def req(req, user=None, pw=None):
        user = load_user(email=user, pw=pw)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_request_files(user=user, req_id=req))

    @staticmethod
    def alldocs(user=None, pw=None):
        rsession = requests.Session()
        login_session(rsession, load_user(email=user, pw=pw))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_documents(rsession=rsession))

    @staticmethod
    def allreqs(user=None, pw=None):
        rsession = requests.Session()
        login_session(rsession, load_user(email=user, pw=pw))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(print_all_requests(rsession=rsession))


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
