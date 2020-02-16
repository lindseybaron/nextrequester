import asyncio

import fire

from util.fetch import download_all_documents, download_all_request_files, print_all_requests


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


if __name__ == '__main__':
    # westlakeinvestigations
    # NextRequest.req('19-7182')  # 0 public, 6 pages requester
    # NextRequest.req('19-7246')  # 0 public, 0 requester
    # NextRequest.req('19-7292')  # 0 public, 1 folder with 1 file requester
    # NextRequest.req('19-7293')  # 0 public, 6 pages requester with 1 folder with 1 file
    NextRequest.req('19-7100')  # 0 public, several pages of requester
    # NextRequest.req('19-3717')  # 1 public, 0 requester
    # NextRequest.req('19-7189')  # 0 public, 3 pages requester
    # Arasod Hupana
    # NextRequest.req('19-6277')  # 0 public, 0 requester
    # NextRequest.req('19-6644')  # 0 public, 1 page requester
    # NextRequest.req('19-6802')  # 0 public, 1 requester
    # NextRequest.req('19-6903')  # 0 public, 1 page requester
    # NextRequest.req('19-6904')  # 0 public, 0 requester
    # NextRequest.req('19-6915')  # 0 public, 1 folder requester
    # NextRequest.req('19-7346')
    # NextRequest.req('19-7347')
    # NextRequest.req('19-7397')
    # NextRequest.req('19-4996')  # 0 public, multiple folders and pages requester
    # NextRequest.alldocs()
    # NextRequest.allreqs()
    # NextRequest.allreqs(login=True)
    # NextRequest.myreqs()
    # next_requester = NextRequest()
    # fire.Fire(next_requester)
