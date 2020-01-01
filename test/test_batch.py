from pages.login.login_page import LoginPage
from pages.records_request.request_page import RequestPage
from util.config import load_user, get_secret
from util.driver import get_driver


class TestRecordRequest:

    def test_load_record_request(self):
        req = '19-4996'

        user = load_user(email=get_secret('email'), pw=get_secret('pw'))
        driver = get_driver()
        LoginPage(driver).login(user['email'], user['pw'])

        request_page = RequestPage(driver, request_id=req)
        request_page.visit()

        assert req in request_page.request_header.text
