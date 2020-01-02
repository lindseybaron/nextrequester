import fire

from pages.documents.documents_page import DocumentsPage
from pages.login.login_page import LoginPage
from pages.records_request.request_page import RecordRequestPage
from util.config import load_user
from util.driver import get_driver


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

        user = load_user(user, pw)

        driver = get_driver(sub_dir='documents')
        LoginPage(driver).login(user['email'], user['pw'])

        docs_page = DocumentsPage(driver)
        docs_page.visit()
        docs_page.download_all_files()


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
