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
