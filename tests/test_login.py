import pytest
from pytest_bdd import scenario, given, when, then, parsers
from playwright.sync_api import Page, expect
import locators

# Scenarios
@scenario('../features/login.feature', 'Successful Login with Valid Credentials')
def test_successful_login():
    pass

@scenario('../features/login.feature', 'Failed Login with Invalid Credentials')
def test_failed_login():
    pass

@scenario('../features/login.feature', 'Login Button Persistence (The "Healer" Test)')
def test_login_button_persistence():
    pass

@scenario('../features/login.feature', 'Navigate to Register Tab')
def test_navigate_to_register():
    pass

@scenario('../features/login.feature', 'Validation for Empty Fields')
def test_validation_empty_fields():
    pass

@scenario('../features/login.feature', 'Validation for Invalid Email Format')
def test_validation_invalid_email():
    pass

# Shared Steps
@given('I am on the Paisa login page (https://paisa.ritadhi.com)')
@given('I am on the Paisa login page')
def go_to_login(page: Page):
    page.goto("https://paisa.ritadhi.com/login")

@given('I am on the "Sign In" tab of the Paisa login page')
def on_sign_in_tab(page: Page):
    page.goto("https://paisa.ritadhi.com/login")
    expect(page.locator(locators.LOGIN_PAGE["sign_in_tab"])).to_be_visible()

# Step Definitions
@when('I enter a valid username and a valid password')
def enter_valid_creds(page: Page):
    # Note: In a real test, use environment variables for credentials
    page.fill(locators.LOGIN_PAGE["email_field"], "test@example.com")
    page.fill(locators.LOGIN_PAGE["password_field"], "password123")

@when('I enter an incorrect username or password')
def enter_invalid_creds(page: Page):
    page.fill(locators.LOGIN_PAGE["email_field"], "wrong@example.com")
    page.fill(locators.LOGIN_PAGE["password_field"], "wrongpass")

@when('I click the "Login" button')
def click_login(page: Page):
    page.click(locators.LOGIN_PAGE["login_button"])

@when('the page finishes loading')
def wait_for_load(page: Page):
    page.wait_for_load_state("networkidle")

@when('I click the "Register" tab')
def click_register(page: Page):
    page.click(locators.LOGIN_PAGE["register_tab"])

@when('I leave the email and password fields empty')
def clear_fields(page: Page):
    page.fill(locators.LOGIN_PAGE["email_field"], "")
    page.fill(locators.LOGIN_PAGE["password_field"], "")

@when(parsers.parse('I enter "{email}" into the email field'))
def enter_email(page: Page, email):
    page.fill(locators.LOGIN_PAGE["email_field"], email)

@then('I should be redirected to the "Dashboard" page')
def check_dashboard_redirect(page: Page):
    expect(page).to_have_url("https://paisa.ritadhi.com/dashboard")

@then('I should see my "Total Balance" widget')
def check_dashboard_widget(page: Page):
    expect(page.locator(locators.DASHBOARD_PAGE["total_balance_widget"])).to_be_visible()

@then('I should see an error message saying "Invalid Credentials"')
def check_error_message(page: Page):
    expect(page.locator(locators.LOGIN_PAGE["error_message"])).to_be_visible()

@then('I should remain on the login page')
def check_login_page_remains(page: Page):
    assert "/login" in page.url

@then('the "Login" button should be visible and enabled')
def check_login_button(page: Page):
    btn = page.locator(locators.LOGIN_PAGE["login_button"])
    expect(btn).to_be_visible()
    expect(btn).to_be_enabled()

@then('its selector should match the entry in locators.py')
def check_locator_match(page: Page):
    # This is a meta-test for the "Healer" concept
    selector = locators.LOGIN_PAGE["login_button"]
    assert page.locator(selector).count() > 0

@then('I should see the registration form')
def check_registration_form(page: Page):
    expect(page.locator(locators.LOGIN_PAGE["sign_up_button"])).to_be_visible()

@then('the "Sign Up" button should be visible')
def check_signup_button(page: Page):
    expect(page.locator(locators.LOGIN_PAGE["sign_up_button"])).to_be_visible()

@then('I should see a browser validation bubble saying "Please fill out this field"')
def check_validation_bubble(page: Page):
    # Checking native HTML5 validation
    validation_message = page.locator(locators.LOGIN_PAGE["email_field"]).evaluate("el => el.validationMessage")
    assert "fill out this field" in validation_message.lower()

@then('I should see a browser validation bubble regarding the "@" character')
def check_email_validation_bubble(page: Page):
    validation_message = page.locator(locators.LOGIN_PAGE["email_field"]).evaluate("el => el.validationMessage")
    assert "@" in validation_message
