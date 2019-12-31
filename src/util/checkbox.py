def check_box(element, deselect=False):
    is_checked = element.get_attribute("checked")
    if deselect:
        if is_checked:
            element.click()
    else:
        if not is_checked:
            element.click()