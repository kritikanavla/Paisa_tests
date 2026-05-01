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
    "total_balance_widget": "text=Total Balance",
}
