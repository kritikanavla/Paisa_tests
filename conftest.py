import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "https://paisa.ritadhi.com",
        "viewport": {"width": 1280, "height": 720},
    }

@pytest.fixture
def login_page(page: Page):
    page.goto("/login")
    return page
