import fire

from pages.login.login_page import LoginPage
from pages.records_request.request_page import RequestPage
from util.driver import get_driver


class NextRequest(object):

    @staticmethod
    def batch(req, user, pw):

        driver = get_driver(req)

        LoginPage(driver).login(user, pw)

        request_page = RequestPage(driver, request_id=req)
        request_page.visit()
        request_page.download_all_files()


if __name__ == '__main__':
    next_requester = NextRequest()
    fire.Fire(next_requester)
