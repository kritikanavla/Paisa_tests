import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "https://paisa.ritadhi.com",
        "viewport": {"width": 1280, "height": 720},
    }

@pytest.fixture
def login_page(page: Page):
    lp = LoginPage(page)
    lp.navigate()
    return lp

@pytest.fixture
def dashboard_page(page: Page):
    return DashboardPage(page)

@pytest.fixture
def logged_in_dashboard(page: Page):
    lp = LoginPage(page)
    lp.navigate()
    # Using dummy credentials - in a real env, use environment variables
    lp.login("test@example.com", "Password123!")
    dp = DashboardPage(page)
    dp.navigate()
    return dp
