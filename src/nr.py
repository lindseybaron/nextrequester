import asyncio

import fire

from nr_functions import download_all_request_files, download_all_documents, print_all_requests, print_my_requests


class NextRequest(object):

    @staticmethod
    def req(req, email=None, pw=None):
        """Get all documents from a single request.

        Args:
            req (str): The unique ID of the request.
            email (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_request_files(email=email, pw=pw, req_id=req))

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

    @staticmethod
    def myreqs(email=None, pw=None, outfile='my_requests.csv'):
        """Print a list of requests submitted by the current user.

        Args:
            email (str): The email address for the user account. Can also be set in secret.yaml.
            pw (str): The password for the user account. Can also be set in secret.yaml.
            outfile (str): Optional parameter to specify the name of the output file.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(print_my_requests(email=email, pw=pw, outfile=outfile))


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
