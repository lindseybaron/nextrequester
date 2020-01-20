class Page:

    url = ""

    def __init__(self, driver, **kwargs):
        self.driver = driver

        for key, value in kwargs.items():
            setattr(self, key, value)

    def visit(self):
        self.driver.get(self.url)
        return self
