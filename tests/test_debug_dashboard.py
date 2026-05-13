import pytest
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage

def test_screenshot_dashboard(logged_in_dashboard: DashboardPage):
    page = logged_in_dashboard.page
    print(f"Current URL: {page.url}")
    page.wait_for_timeout(5000) # Wait for elements to settle
    page.screenshot(path="dashboard_live.png")
    
    # Print all button texts
    buttons = page.query_selector_all("button")
    print("Buttons found:")
    for btn in buttons:
        print(f"  - {btn.inner_text()}")
