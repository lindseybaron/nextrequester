import asyncio

import fire

from util.fetch import download_all_documents, download_all_request_files, print_all_requests


class NextRequest(object):

    @staticmethod
    def req(req, email=None, pw=None, dl=True):
        """Get all documents from a single request.

        Args:
            req (str): The unique ID of the request.
            email (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_request_files(email=email, pw=pw, req_id=req, download_files=dl))

    @staticmethod
    def alldocs(email=None, pw=None):
        """Download all the documents from the 'All Documents' section.
            This includes all public documents and any documents visible to the logged in user if logged in.

        Args:
            email (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_documents(email=email, pw=pw))

    @staticmethod
    def allreqs(email=None, pw=None):
        """Fetch all the requests from the 'All Requests' section.
            This includes all public requests and any requests visible to the logged in user if logged in.

        Args:
            email (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(print_all_requests(email=email, pw=pw))


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
