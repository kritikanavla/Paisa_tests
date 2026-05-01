from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import locators

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.widgets = {
            "total_capital": page.locator(locators.DASHBOARD_PAGE["total_capital"]),
            "beta_exposure": page.locator(locators.DASHBOARD_PAGE["beta_exposure"]),
            "unrealized_pnl": page.locator(locators.DASHBOARD_PAGE["unrealized_pnl"]),
            "winning_positions": page.locator(locators.DASHBOARD_PAGE["winning_positions"]),
            "actions_required": page.locator(locators.DASHBOARD_PAGE["actions_required"]),
        }
        self.active_positions_table = page.locator(locators.DASHBOARD_PAGE["active_positions_table"])
        self.deep_analysis_label = page.locator(locators.DASHBOARD_PAGE["deep_analysis_label"])
        self.sidebar_hunter = page.locator(locators.DASHBOARD_PAGE["sidebar_hunter"])
        self.sidebar_discovery = page.locator(locators.DASHBOARD_PAGE["sidebar_discovery"])
        self.system_status = page.locator(locators.DASHBOARD_PAGE["system_status"])
        self.footer_stable = page.locator(locators.DASHBOARD_PAGE["footer_stable"])
        self.record_trade_btn = page.locator(locators.DASHBOARD_PAGE["record_trade_btn"])
        self.market_discoveries_btn = page.locator(locators.DASHBOARD_PAGE["market_discoveries_btn"])
        self.global_search = page.locator(locators.DASHBOARD_PAGE["global_search"])
        self.sync_status = page.locator(locators.DASHBOARD_PAGE["sync_status"])
        self.logout_icon = page.locator(locators.DASHBOARD_PAGE["logout_icon"])
        self.sector_mix_chart = page.locator(locators.DASHBOARD_PAGE["sector_mix_chart"])

    def is_visible(self):
        expect(self.page).to_have_url("/dashboard")
        for widget in self.widgets.values():
            expect(widget).to_be_visible()

    def navigate(self):
        super().navigate("/dashboard")

    def click_ticker_row(self, ticker: str):
        self.page.click(f"text={ticker}")

    def search_ticker(self, ticker: str):
        self.global_search.fill(ticker)
        self.global_search.press("Enter")

    def click_market_discoveries(self):
        self.market_discoveries_btn.click()

    def logout(self):
        self.logout_icon.click()

    def get_sync_status_text(self):
        return self.sync_status.inner_text()
