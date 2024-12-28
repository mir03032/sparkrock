import time

import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Create a new python fixture
@pytest.fixture(scope="module")
def driver():
    # Use Webdriver manager to install the correct chromedriver version
    service = Service(ChromeDriverManager().install())

    # Initialize the driver
    driver = webdriver.Chrome(service=service)

    # Run tests using driver
    yield driver
    # Clean up after running cases
    driver.quit()

# Automating example test case 1
# We can also make user login function a fixture, that way we can just call this fixture in our test case
def test_user_login(driver):
    # Get the login page
    driver.get("https://bankingexample.com/login")

    # Find username and password fields
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    # Enter Credentials
    username_field.send_keys("testuser")
    password_field.send_keys("password")

    # submit the login form
    password_field.send_keys(Keys.RETURN)

    # Wait for page to load, check for an element on the login dashboard
    time.sleep(3)
    # Looking for the word "Welcome" after successful login
    welcome_message = driver.find_element(By.XPATH, "//dic[contains(text(), 'Welcome')]")

    # Assert that login was successful
    # Show error message "Login failed: Welcome message not found" is login fails
    assert welcome_message.is_displayed(), "Login failed: Welcome message not found"


# Automating example test case 2
def test_fund_transfer(driver):
    # Logging in just like test case 1
    driver.get("https://bankingexample.com/login")

    # Find username and password fields
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    # Enter Credentials
    username_field.send_keys("testuser")
    password_field.send_keys("password")

    # submit the login form
    password_field.send_keys(Keys.RETURN)

    # Wait for page to load, check for an element on the login dashboard
    time.sleep(3)
    # Looking for the word "Welcome" after successful login
    welcome_message = driver.find_element(By.XPATH, "//div[contains(text(), 'Welcome')]")

    # Assert that login was successful
    # Show error message "Login failed: Welcome message not found" is login fails
    assert welcome_message.is_displayed(), "Login failed: Welcome message not found"

    # Navigate to money transfer page
    driver.get("https://bankingexample.com/transfer")

    # Select from and to accounts
    from_account = driver.find_element(By.ID, "from_account")
    to_account = driver.find_element(By.ID, "to_account")

    # We are transferring from checking to savings account
    from_account.send_keys("Checking")
    to_account.send_keys("Savings")

    # Enter the transfer amount and submit
    transfer_amount_field = driver.find_element(By.ID, "amount")
    transfer_amount_field.send_keys("1000.00")

    transfer_button = driver.find_element(By.ID, "transfer_button")
    transfer_button.click()

    # Wait for the transfer to complete
    time.sleep(3)

    success_message = driver.find_element(By.XPATH, "//dic[contains(text(), 'Transfer successful')]")

    # Assert, if fails display the error message
    assert  success_message.is_displayed(), "Transfer failed"

    # Verify the balances after the transfer
    from_account_balance = driver.find_element(By.ID, "checking_balance").text
    to_account_balance = driver.find_element(By.ID, "savings_balance").text

    # Assert the new balances, make assumptions that from account still has more than 1000 bucks
    # We can also do a before and after check, which might be a better option
    assert float(from_account_balance) >= 1000.00, "From account balance not updated"
    assert float(to_account_balance) >= 1000.00, "To account balance not updated"


"""I have made some assumptions here. The banking website is just for demo, the IDs, XPaths those are also only for demo.
 Thank you for your time."""

