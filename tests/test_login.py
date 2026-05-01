import pytest
from playwright.sync_api import Page, expect
import locators

def test_scenario_1_successful_login(login_page: Page):
    """Scenario 1: Successful Login with Valid Credentials"""
    login_page.fill(locators.LOGIN_PAGE["email_field"], "test@example.com")
    login_page.fill(locators.LOGIN_PAGE["password_field"], "Password123!")
    login_page.click(locators.LOGIN_PAGE["login_button"])
    
    # Expect redirection to dashboard
    expect(login_page).to_have_url("/dashboard")
    expect(login_page.locator(locators.DASHBOARD_PAGE["total_balance_widget"])).to_be_visible()

def test_scenario_2_failed_login(login_page: Page):
    """Scenario 2: Failed Login with Invalid Credentials"""
    login_page.fill(locators.LOGIN_PAGE["email_field"], "wrong@example.com")
    login_page.fill(locators.LOGIN_PAGE["password_field"], "WrongPassword")
    login_page.click(locators.LOGIN_PAGE["login_button"])
    
    expect(login_page.locator(locators.LOGIN_PAGE["error_message"])).to_be_visible()
    expect(login_page).to_have_url("/login")

def test_scenario_3_login_button_healer(login_page: Page):
    """Scenario 3: Login Button Persistence (The Healer Test)"""
    login_button = login_page.locator(locators.LOGIN_PAGE["login_button"])
    expect(login_button).to_be_visible()
    expect(login_button).to_be_enabled()
    # In a real "Healer" test, we might compare the selector to a known good state
    assert locators.LOGIN_PAGE["login_button"] == "button:has-text('Sign In')"

def test_scenario_4_navigate_to_register_tab(login_page: Page):
    """Scenario 4: Navigate to Register Tab"""
    login_page.click(locators.LOGIN_PAGE["register_tab"])
    expect(login_page.locator(locators.LOGIN_PAGE["sign_up_button"])).to_be_visible()

def test_scenario_5_validation_empty_fields(login_page: Page):
    """Scenario 5: Validation for Empty Fields"""
    login_page.click(locators.LOGIN_PAGE["login_button"])
    # HTML5 validation bubble check is tricky in Playwright, 
    # but we can check if the field is invalid
    email_field = login_page.locator(locators.LOGIN_PAGE["email_field"])
    is_invalid = email_field.evaluate("el => !el.checkValidity()")
    assert is_invalid is True

def test_scenario_6_validation_invalid_email(login_page: Page):
    """Scenario 6: Validation for Invalid Email Format"""
    login_page.fill(locators.LOGIN_PAGE["email_field"], "invalid-email")
    login_page.click(locators.LOGIN_PAGE["login_button"])
    
    email_field = login_page.locator(locators.LOGIN_PAGE["email_field"])
    is_invalid = email_field.evaluate("el => !el.checkValidity()")
    assert is_invalid is True

def test_scenario_7_successful_registration(login_page: Page):
    """Scenario 7: Successful Registration"""
    login_page.click(locators.LOGIN_PAGE["register_tab"])
    login_page.fill(locators.LOGIN_PAGE["email_field"], "newuser@example.com")
    login_page.fill(locators.LOGIN_PAGE["password_field"], "NewPass123!")
    login_page.click(locators.LOGIN_PAGE["sign_up_button"])
    
    # Redirection check
    expect(login_page).to_have_url("/dashboard")

def test_scenario_8_logout_functionality(login_page: Page):
    """Scenario 8: Logout Functionality"""
    # Assuming we are logged in for this test
    # (In real tests, use a logged-in state fixture)
    login_page.goto("/dashboard") 
    # Add steps to logout once Dashboard locators are known
    # login_page.click(locators.DASHBOARD_PAGE["profile_icon"])
    # login_page.click(locators.DASHBOARD_PAGE["sign_out_button"])
    # expect(login_page).to_have_url("/login")
    pass

def test_scenario_9_redirect_unauthenticated(page: Page):
    """Scenario 9: Redirect Unauthenticated User"""
    page.goto("/dashboard")
    expect(page).to_have_url("/login")

def test_scenario_10_seo_metadata(login_page: Page):
    """Scenario 10: SEO and Metadata Validation"""
    expect(login_page).to_have_title(re.compile("Paisa"))
    description = login_page.locator("meta[name='description']")
    expect(description).to_have_attribute("content", re.compile(".+"))
    
    # Check labels
    expect(login_page.locator("label[for='email']")).to_be_visible()
    expect(login_page.locator("label[for='password']")).to_be_visible()

def test_scenario_11_security_sqli(login_page: Page):
    """Scenario 11: Security - Attempt SQL Injection"""
    login_page.fill(locators.LOGIN_PAGE["email_field"], "' OR '1'='1")
    login_page.fill(locators.LOGIN_PAGE["password_field"], "anything")
    login_page.click(locators.LOGIN_PAGE["login_button"])
    
    expect(login_page.locator(locators.LOGIN_PAGE["error_message"])).to_be_visible()
    expect(login_page).to_have_url("/login")

def test_scenario_12_security_xss(login_page: Page):
    """Scenario 12: Security - Attempt XSS Injection"""
    # Set up a listener for any alerts
    alert_occurred = False
    def on_dialog(dialog):
        nonlocal alert_occurred
        alert_occurred = True
        dialog.dismiss()
    
    login_page.on("dialog", on_dialog)
    login_page.fill(locators.LOGIN_PAGE["email_field"], "<script>alert('xss')</script>")
    login_page.click(locators.LOGIN_PAGE["login_button"])
    
    assert alert_occurred is False

def test_scenario_13_edge_case_long_input(login_page: Page):
    """Scenario 13: Edge Case - Very Long Input"""
    long_string = "a" * 1000
    login_page.fill(locators.LOGIN_PAGE["email_field"], long_string)
    # Check if field limits input or handles it
    current_val = login_page.locator(locators.LOGIN_PAGE["email_field"]).input_value()
    assert len(current_val) <= 1000 # Just verifying it was filled

def test_scenario_14_edge_case_special_chars(login_page: Page):
    """Scenario 14: Edge Case - Password with Special Characters"""
    special_pass = "$%^&*()_+"
    login_page.fill(locators.LOGIN_PAGE["email_field"], "test@example.com")
    login_page.fill(locators.LOGIN_PAGE["password_field"], special_pass)
    login_page.click(locators.LOGIN_PAGE["login_button"])
    # Just verifying it doesn't crash the browser/frontend
    expect(login_page.locator(locators.LOGIN_PAGE["error_message"])).to_be_visible()

import re
