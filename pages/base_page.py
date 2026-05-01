from playwright.sync_api import Page, Response

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> Response:
        return self.page.goto(url)

    def wait_for_load_state(self, state: str = "networkidle"):
        self.page.wait_for_load_state(state)
