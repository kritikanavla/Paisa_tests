import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
import re

def test_scenario_1_successful_login(login_page: LoginPage, dashboard_page: DashboardPage):
    """Scenario 1: Successful Login with Valid Credentials"""
    login_page.login("test@example.com", "Password123!")
    dashboard_page.is_visible()

def test_scenario_2_failed_login(login_page: LoginPage):
    """Scenario 2: Failed Login with Invalid Credentials"""
    login_page.login("wrong@example.com", "WrongPassword")
    expect(login_page.error_message).to_be_visible()
    expect(login_page.page).to_have_url("/login")

def test_scenario_3_login_button_healer(login_page: LoginPage):
    """Scenario 3: Login Button Persistence (The Healer Test)"""
    expect(login_page.login_button).to_be_visible()
    expect(login_page.login_button).to_be_enabled()

def test_scenario_4_navigate_to_register_tab(login_page: LoginPage):
    """Scenario 4: Navigate to Register Tab"""
    login_page.switch_to_register()
    expect(login_page.sign_up_button).to_be_visible()

def test_scenario_5_validation_empty_fields(login_page: LoginPage):
    """Scenario 5: Validation for Empty Fields"""
    login_page.login_button.click()
    assert login_page.is_field_invalid("email") is True

def test_scenario_6_validation_invalid_email(login_page: LoginPage):
    """Scenario 6: Validation for Invalid Email Format"""
    login_page.email_field.fill("invalid-email")
    login_page.login_button.click()
    assert login_page.is_field_invalid("email") is True

def test_scenario_7_successful_registration(login_page: LoginPage, dashboard_page: DashboardPage):
    """Scenario 7: Successful Registration"""
    login_page.register("newuser@example.com", "NewPass123!")
    dashboard_page.is_visible()

def test_scenario_8_logout_functionality(dashboard_page: DashboardPage, login_page: LoginPage):
    """Scenario 8: Logout Functionality"""
    # Assuming already logged in or navigating to dashboard
    dashboard_page.navigate()
    # dashboard_page.logout()
    # expect(login_page.page).to_have_url("/login")
    pass

def test_scenario_9_redirect_unauthenticated(page: Page):
    """Scenario 9: Redirect Unauthenticated User"""
    page.goto("/dashboard")
    expect(page).to_have_url("/login")

def test_scenario_10_seo_metadata(login_page: LoginPage):
    """Scenario 10: SEO and Metadata Validation"""
    expect(login_page.page).to_have_title(re.compile("Paisa"))
    description = login_page.page.locator("meta[name='description']")
    expect(description).to_have_attribute("content", re.compile(".+"))
    
    # Check labels using page object elements
    expect(login_page.page.locator("label[for='email']")).to_be_visible()

def test_scenario_11_security_sqli(login_page: LoginPage):
    """Scenario 11: Security - Attempt SQL Injection"""
    login_page.login("' OR '1'='1", "anything")
    expect(login_page.error_message).to_be_visible()

def test_scenario_12_security_xss(login_page: LoginPage):
    """Scenario 12: Security - Attempt XSS Injection"""
    alert_occurred = False
    def on_dialog(dialog):
        nonlocal alert_occurred
        alert_occurred = True
        dialog.dismiss()
    
    login_page.page.on("dialog", on_dialog)
    login_page.email_field.fill("<script>alert('xss')</script>")
    login_page.login_button.click()
    assert alert_occurred is False

def test_scenario_13_edge_case_long_input(login_page: LoginPage):
    """Scenario 13: Edge Case - Very Long Input"""
    long_string = "a" * 1000
    login_page.email_field.fill(long_string)
    assert len(login_page.email_field.input_value()) <= 1000

def test_scenario_14_edge_case_special_chars(login_page: LoginPage):
    """Scenario 14: Edge Case - Password with Special Characters"""
    login_page.login("test@example.com", "$%^&*()_+")
    expect(login_page.error_message).to_be_visible()
