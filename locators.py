# Locators for Paisa Application

LOGIN_PAGE = {
    "email_field": "id=email",
    "password_field": "id=password",
    "login_button": "button:has-text('Sign In')",  # Mapped to "Sign In" as seen on site
    "error_message": "text=Invalid email or password.",
}

DASHBOARD_PAGE = {
    "total_balance_widget": "text=Total Balance",
}
