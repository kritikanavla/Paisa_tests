Feature: Login Functionality

  Scenario: Successful Login with Valid Credentials
    Given I am on the Paisa login page (https://paisa.ritadhi.com)
    When I enter a valid username and a valid password
    And I click the "Login" button
    Then I should be redirected to the "Dashboard" page
    And I should see my "Total Balance" widget

  Scenario: Failed Login with Invalid Credentials
    Given I am on the Paisa login page
    When I enter an incorrect username or password
    And I click the "Login" button
    Then I should see an error message saying "Invalid Credentials"
    And I should remain on the login page

  Scenario: Login Button Persistence (The "Healer" Test)
    Given I am on the Paisa login page
    When the page finishes loading
    Then the "Login" button should be visible and enabled
    And its selector should match the entry in locators.py

  Scenario: Navigate to Register Tab
    Given I am on the "Sign In" tab of the Paisa login page
    When I click the "Register" tab
    Then I should see the registration form
    And the "Sign Up" button should be visible

  Scenario: Validation for Empty Fields
    Given I am on the Paisa login page
    When I leave the email and password fields empty
    And I click the "Login" button
    Then I should see a browser validation bubble saying "Please fill out this field"

  Scenario: Validation for Invalid Email Format
    Given I am on the Paisa login page
    When I enter "invalid-email" into the email field
    And I click the "Login" button
    Then I should see a browser validation bubble regarding the "@" character

  Scenario: Successful Registration
    Given I am on the "Register" tab of the Paisa login page
    When I enter a new email and a valid password
    And I click the "Sign Up" button
    Then I should be redirected to the "Dashboard" page
    And I should see a "Registration Successful" message

  Scenario: Logout Functionality
    Given I am logged into the Paisa application
    When I click the "Profile" icon
    And I click the "Sign Out" button
    Then I should be redirected back to the "Login" page
    And I should not be able to access the "Dashboard" via URL

  Scenario: Redirect Unauthenticated User
    Given I am not logged in
    When I attempt to navigate directly to "https://paisa.ritadhi.com/dashboard"
    Then I should be automatically redirected to the login page

  Scenario: SEO and Metadata Validation
    Given I am on the Paisa login page
    Then the page title should contain "Paisa"
    And the page should have a "description" meta tag for search engines
    And all input fields should have associated labels for accessibility

  Scenario: Security - Attempt SQL Injection
    Given I am on the Paisa login page
    When I enter "' OR '1'='1" into the email field
    And I enter "password" into the password field
    And I click the "Login" button
    Then I should see an "Invalid Credentials" error
    And I should not be logged in

  Scenario: Security - Attempt XSS Injection
    Given I am on the Paisa login page
    When I enter "<script>alert('xss')</script>" into the email field
    And I click the "Login" button
    Then the script should not execute
    And I should see an error message

  Scenario: Edge Case - Very Long Input
    Given I am on the Paisa login page
    When I enter a string of 1000 characters into the email field
    Then the input should be truncated or show a validation error

  Scenario: Edge Case - Password with Special Characters
    Given I am on the Paisa login page
    When I enter a password containing "$%^&*()_+"
    And I click the "Login" button
    Then it should be processed as a valid password string
