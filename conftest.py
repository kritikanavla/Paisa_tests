import pytest
import json
import os
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "https://paisa.example.com",
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
    # Load trade data from JSON
    trade_data_path = os.path.join(os.path.dirname(__file__), "trade_data.json")
    with open(trade_data_path, "r") as f:
        trades = json.load(f)

    # FAST MOCKING LAYER: Intercept API calls to populate trades instantly
    # We mock multiple common patterns to ensure the dashboard picks it up
    def handle_positions(route):
        route.fulfill(status=200, json=trades)

    page.route("**/api/positions", handle_positions)
    page.route("**/api/trades", handle_positions)
    page.route("**/api/user/positions", handle_positions)
    page.route("**/api/dashboard", lambda route: route.fulfill(
        status=200, 
        json={"summary": {"total_capital": 105000, "pnl": 21.38}, "positions": trades}
    ))

    lp = LoginPage(page)
    lp.navigate()
    # Bypass real login if possible or use real ones if needed
    # For speed, we'll assume the mock handles the "logged in" state check for these endpoints
    lp.login(os.environ.get("PAISA_TEST_EMAIL", "test_user_a@example.com"), os.environ.get("PAISA_TEST_PASSWORD", "Password123!"))
    
    dp = DashboardPage(page)
    dp.navigate()
    return dp

