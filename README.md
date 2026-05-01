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
