# Locators for Paisa Application

LOGIN_PAGE = {
    "email_field": "id=email",
    "password_field": "id=password",
    "login_button": "button:has-text('Sign In')",  # Mapped to "Sign In" as seen on site
    "register_tab": "button:has-text('Register')",
    "sign_in_tab": "button:has-text('Sign In')",
    "error_message": "text=Invalid email or password.",
    "sign_up_button": "button:has-text('Sign Up')",
}

DASHBOARD_PAGE = {
    "total_capital": "text=Total Capital",
    "beta_exposure": "text=Beta-Weighted Exposure",
    "unrealized_pnl": "text=Unrealized P&L",
    "winning_positions": "text=Winning Positions",
    "actions_required": "text=Actions Required",
    "active_positions_table": "table:has-text('Active Positions')",
    "deep_analysis_label": "text=Deep Analysis Pick",
    "sidebar_hunter": "a:has-text('Hunter')",
    "sidebar_discovery": "a:has-text('Discovery')",
    "system_status": "text=FastAPI Connected",
    "footer_stable": "text=stable",
    "record_trade_btn": "button:has-text('Record New Trade')",
    "sector_mix_chart": "canvas, svg, .chart-container", # Generic chart selectors
}
