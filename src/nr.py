import fire

from pages.login.login_page import LoginPage
from pages.records_request.request_page import RequestPage
from util.config import load_user
from util.driver import get_driver


class NextRequest(object):

    @staticmethod
    def batch(req, user=None, pw=None):

        user = load_user(user, pw)

        driver = get_driver(req)

        LoginPage(driver).login(user['email'], user['pw'])

        request_page = RequestPage(driver, request_id=req)
        request_page.visit()
        request_page.download_all_files()


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
