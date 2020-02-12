import polling
from selenium.common.exceptions import StaleElementReferenceException

from util.constants import WAIT_INTERVAL, LONG_WAIT_TIME


def flaky_find(parent_element, locator):
    stale = True
    count = 0
    max = 10

    while stale and count < max:
        try:
            polling.poll(
                lambda: len(parent_element.find_elements(*locator)) > 0,
                step=WAIT_INTERVAL,
                timeout=LONG_WAIT_TIME,
            )
            stale = False
        except StaleElementReferenceException:
            stale = True
            count = count + 1

    return parent_element.find_element(*locator)
