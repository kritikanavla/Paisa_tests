# Paisa Tests

Repository for testing the Paisa application.

## Testing Structure

- `features/`: Contains Gherkin `.feature` files defining the test scenarios.
- `locators.py`: Centralized file for element selectors.

## Current Scenarios

### Login Functionality (`features/login.feature`)
1. **Successful Login**: Validates redirection to Dashboard and visibility of core widgets.
2. **Failed Login**: Validates error handling for invalid credentials.
3. **Healer Test**: Ensures the login button remains stable and matches defined locators.
4. **...and 11 more scenarios** covering registration, security, and edge cases.

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
