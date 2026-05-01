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
