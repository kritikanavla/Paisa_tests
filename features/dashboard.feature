Feature: Dashboard Functionality

  Scenario 1: Dashboard Overview Visibility
    Given I am logged in and on the Dashboard page
    Then I should see the "Total Capital" widget
    And I should see the "Beta-Weighted Exposure" widget
    And I should see the "Unrealized P&L" widget
    And I should see the "Winning Positions" widget
    And I should see the "Actions Required" widget

  Scenario 2: Active Positions Table
    Given I am logged in and on the Dashboard page
    Then I should see the "Active Positions & Risk Shield" table
    And the table should contain columns for "Ticker", "Strategy", "Current Price", and "P&L%"

  Scenario 3: AI Hunter Integration
    Given I am logged in and on the Dashboard page
    When I look at the "Active Positions" table
    Then I should see trades flagged as "Deep Analysis Pick" by the AI Hunter

  Scenario 4: Sidebar Navigation
    Given I am logged in and on the Dashboard page
    Then the sidebar should contain links to:
      | Page      |
      | Discovery |
      | Hunter    |
      | Analysis  |
      | Options   |
      | Risk Lab  |

  Scenario 5: System Health Monitoring
    Given I am logged in and on the Dashboard page
    Then the system status should show "FastAPI Connected"
    And the footer should indicate "System Stable"
    And the data health should be at "100%"

  Scenario 6: Quick Actions
    Given I am logged in and on the Dashboard page
    Then I should see the "Record New Trade" button
    And I should see the "Market Discoveries" button

  Scenario 7: Responsive Analytics Chart
    Given I am logged in and on the Dashboard page
    Then I should see the "Sector Mix" or "Exposure Weights" chart
    And it should be interactive and display data distribution

  Scenario 8: Detailed Trade Analysis Navigation
    Given I am on the Dashboard page with active positions
    When I click on a ticker row (e.g., "NVDA") in the Active Positions table
    Then I should be navigated to the "Analysis" page for that ticker
    And the URL should contain "?ticker=NVDA"

  Scenario 9: Market Discoveries Redirection
    Given I am on the Dashboard page
    When I click the "Market Discoveries" button in the Actions section
    Then I should be navigated to the "/discovery" page

  Scenario 10: Global Ticker Search
    Given I am on the Dashboard page
    Then I should see a global "Search ticker..." input box at the top
    When I enter a ticker symbol and press Enter
    Then I should see the analysis for that ticker

  Scenario 11: Data Sync Initialization
    Given I am on the Dashboard page
    When the page is refreshed
    Then I should see a "Sync Paisa" status message during data loading
    And the dashboard should populate with the latest data once sync is complete

  Scenario 12: Logout via Icon
    Given I am on the Dashboard page
    When I click the "Logout" icon next to the profile label
    Then I should be logged out and redirected to the login page
