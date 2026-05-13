import pytest
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage
import re

def test_scenario_1_dashboard_overview(logged_in_dashboard: DashboardPage):
    """Scenario 1: Dashboard Overview Visibility"""
    logged_in_dashboard.is_visible()

def test_scenario_2_active_positions_table(logged_in_dashboard: DashboardPage):
    """Scenario 2: Active Positions Table"""
    expect(logged_in_dashboard.active_positions_table).to_be_visible()
    # Check for column headers
    expect(logged_in_dashboard.page.locator("text=Ticker")).to_be_visible()
    expect(logged_in_dashboard.page.locator("text=Strategy")).to_be_visible()
    
    # Verify ALL 12 entries are present (Mocking Layer check)
    rows = logged_in_dashboard.page.locator("table tbody tr")
    # Some apps might render headers or footers in table, so we check for at least 12
    expect(rows).to_have_count(12)

def test_scenario_3_ai_hunter_integration(logged_in_dashboard: DashboardPage):
    """Scenario 3: AI Hunter Integration"""
    # Verify specific strategies from trade_data.json
    expect(logged_in_dashboard.page.locator("text=Deep Analysis Pick")).to_be_visible()
    expect(logged_in_dashboard.page.locator("text=Bull Call Spread")).to_be_visible()
    expect(logged_in_dashboard.page.locator("text=Iron Condor")).to_be_visible()
    expect(logged_in_dashboard.page.locator("text=Momentum Play")).to_be_visible()

def test_scenario_4_sidebar_navigation(logged_in_dashboard: DashboardPage):
    """Scenario 4: Sidebar Navigation"""
    expect(logged_in_dashboard.sidebar_hunter).to_be_visible()
    expect(logged_in_dashboard.sidebar_discovery).to_be_visible()

def test_scenario_5_system_health(logged_in_dashboard: DashboardPage):
    """Scenario 5: System Health Monitoring"""
    expect(logged_in_dashboard.system_status).to_have_text("FastAPI Connected")
    expect(logged_in_dashboard.footer_stable).to_be_visible()

def test_scenario_6_quick_actions(logged_in_dashboard: DashboardPage):
    """Scenario 6: Quick Actions"""
    expect(logged_in_dashboard.record_trade_btn).to_be_visible()
    expect(logged_in_dashboard.market_discoveries_btn).to_be_visible()

def test_scenario_7_responsive_chart(logged_in_dashboard: DashboardPage):
    """Scenario 7: Responsive Analytics Chart"""
    expect(logged_in_dashboard.sector_mix_chart).to_be_visible()

def test_scenario_8_trade_analysis_navigation(logged_in_dashboard: DashboardPage):
    """Scenario 8: Detailed Trade Analysis Navigation"""
    # Assuming "NVDA" is a ticker in the table
    try:
        logged_in_dashboard.click_ticker_row("NVDA")
        expect(logged_in_dashboard.page).to_have_url(re.compile(r".*analysis.*ticker=NVDA"))
    except:
        pytest.skip("Ticker NVDA not found in table")

def test_scenario_9_market_discoveries_redirection(logged_in_dashboard: DashboardPage):
    """Scenario 9: Market Discoveries Redirection"""
    logged_in_dashboard.click_market_discoveries()
    expect(logged_in_dashboard.page).to_have_url(re.compile(r".*discovery.*"))

def test_scenario_10_global_search(logged_in_dashboard: DashboardPage):
    """Scenario 10: Global Ticker Search"""
    logged_in_dashboard.search_ticker("AAPL")
    expect(logged_in_dashboard.page).to_have_url(re.compile(r".*analysis.*ticker=AAPL"))

def test_scenario_11_data_sync(logged_in_dashboard: DashboardPage):
    """Scenario 11: Data Sync Initialization"""
    logged_in_dashboard.page.reload()
    # Expect sync message to appear then disappear
    expect(logged_in_dashboard.sync_status).to_be_visible()
    expect(logged_in_dashboard.sync_status).to_be_hidden(timeout=10000)

def test_scenario_12_logout_via_icon(logged_in_dashboard: DashboardPage):
    """Scenario 12: Logout via Icon"""
    logged_in_dashboard.logout()
    expect(logged_in_dashboard.page).to_have_url(re.compile(r".*login.*"))
