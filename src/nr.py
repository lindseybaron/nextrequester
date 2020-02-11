import asyncio

import fire
import requests

from util.auth import login_session
from util.config import load_user
from util.fetch import download_all_documents, download_all_request_files, print_all_requests


class NextRequest(object):

    @staticmethod
    def req(req, user=None, pw=None):
        """Get all documents from a single request.

        Args:
            req (str): The unique ID of the request.
            user (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        user = load_user(email=user, pw=pw)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_request_files(user=user, req_id=req))

    @staticmethod
    def alldocs(user=None, pw=None):
        """Download all the documents from the 'All Documents' section.
            This includes all public documents and any documents visible to the logged in user if logged in.

        Args:
            user (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        rsession = requests.Session()
        login_session(rsession, load_user(email=user, pw=pw))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_documents(rsession=rsession))

    @staticmethod
    def allreqs(user=None, pw=None):
        """Fetch all the requests from the 'All Requests' section.
            This includes all public requests and any requests visible to the logged in user if logged in.

        Args:
            user (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        rsession = requests.Session()
        login_session(rsession, load_user(email=user, pw=pw))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(print_all_requests(rsession=rsession))


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
