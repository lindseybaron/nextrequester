from selenium.webdriver.common.by import By


def print_pagy(pagy_element):
    """Print the given pagination to the console.

    Args:
        pagy_element (WebElement): The pagination element to parse and print.
    """
    pages = pagy_element.find_elements(By.CLASS_NAME, 'page')
    pagy_string = []
    for page in pages:
        if 'NEXT' in page.text.upper():
            if 'disabled' in page.get_attribute('class'):
                pagy_string.append(page.text.split()[0])
            else:
                pagy_string.append('[{}]'.format(page.text.split()[0]))
        elif 'PREV' in page.text.upper():
            if 'disabled' in page.get_attribute('class'):
                pagy_string.append(page.text.split()[1])
            else:
                pagy_string.append('[{}]'.format(page.text.split()[1]))
        elif '…' in page.text:
            pagy_string.append(page.text)
        elif 'active' not in page.get_attribute('class'):
            pagy_string.append('[{}]'.format(page.text))
        else:
            pagy_string.append(page.text)

    print(' '.join(pagy_string))
