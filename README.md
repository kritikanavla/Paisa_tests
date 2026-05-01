# Paisa Tests

Repository for testing the Paisa application.

## Testing Structure

- `features/`: Contains Gherkin `.feature` files defining the test scenarios.
- `locators.py`: Centralized file for element selectors.

## Current Scenarios

### Login Functionality (`features/login.feature`)
1. **Successful Login**: Validates redirection to Dashboard and visibility of core widgets.
2. **...and 13 more scenarios** covering registration, security, and edge cases.

### Dashboard Functionality (`features/dashboard.feature`)
1. **Dashboard Overview**: Verifies visibility of all 5 summary widgets.
2. **Active Positions**: Validates the central trade table and its AI Hunter integrations.
3. **System Monitoring**: Checks real-time health stats and API connection state.
4. **Navigation & Actions**: Verifies sidebar links and quick action buttons.

## Automation

The repository includes a Playwright-based automation suite in Python.

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Playwright browsers:
   ```bash
   playwright install
   ```

### Running Tests
Run all tests:
```bash
pytest
```

Run specific login tests:
```bash
pytest tests/test_login.py
```
