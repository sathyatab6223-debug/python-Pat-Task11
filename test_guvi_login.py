# =============================================================================
# PAT Task-11: Selenium & Pytest Automation for GUVI Login
# Purpose: Automate login and create Positive/Negative test cases for validation.
# =============================================================================

# --- Imports ---
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time # Used for simple sleep delays (though explicit waits are generally preferred)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # Explicit wait conditions






# --- Pytest Fixture: Setup and Teardown ---
@pytest.fixture(scope="function")
def driver():
    """
    Initializes the Chrome WebDriver (Setup).
    Configures browser options (maximized).
    Navigates to the base URL (https://www.guvi.in/).
    Uses 'yield' to pass the driver to the tests.
    Performs cleanup by quitting the browser after each test (Teardown).
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.guvi.in/")
    driver.implicitly_wait(2) # Sets a global implicit wait time
    yield driver
    driver.quit() # Closes the browser after the test function is done (Task Requirement: Close the browser)


# --- Test Case 1: URL Validation (Positive Test) ---
def test_validate_url(driver):
    """
    Validates the URL redirection after clicking the 'Sign up/Login' button.
    (Task Requirement 1: Validate the URL of the Login button to be https://www.guvi.in/sign-in/)
    This is a POSITIVE test case.
    """
    try:
        login_button = driver.find_element(By.ID, "login-btn")
        login_button.click()
        current_url = driver.current_url
        expected_url = 'https://www.guvi.in/sign-in/'

        # Assertion for successful redirection

        assert current_url in expected_url, f"URL missmatch Got: {current_url}  Expected: {expected_url} "
        print(f" Login URL validated successfully: {current_url}")
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")


# --- Test Case 2: Element Visibility/Enabled State (Positive Test) ---
def test_02_validate_username_password_visible_enabled(driver):
    """
    Validates that the Username and Password input fields are visible and enabled.
    (Task Requirement 2: Validate that the Username and Password Input boxes are visible and enabled)
    This is a POSITIVE test case.
    """
    try:
        # Navigate directly to sign-in page for test execution
        driver.get('https://www.guvi.in/sign-in/')
        email_field = driver.find_element(By.ID, "email")
        passwd_field = driver.find_element(By.ID,"password" )

        # Validate visibility (is_displayed())
        assert email_field.is_displayed(), f"Email field is not displayed: {email_field.is_displayed()}"
        assert passwd_field.is_displayed(), f"Password field is not displayed: {passwd_field.is_displayed()}"

        # Validate enabled state (is_enabled())
        assert email_field.is_enabled(), "Username field is not enabled"
        assert passwd_field.is_enabled(), "Password field is not enabled"

        print("✓ Username and Password fields are visible and enabled")

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")


# --- Test Case 3: Submit Button Validation (Positive Test) ---
def test_03_validate_submit_button_working (driver):
    """
    Validates that the Submit/Login button is visible, enabled, and clickable.
    (Task Requirement 3: Validate that the Submit button is working properly)
    This is a POSITIVE test case for the element's state.
    """
    try :
        driver.get('https://www.guvi.in/sign-in/')
        submit_button = driver.find_element(By.XPATH, '//a[@id="login-btn"]')
        time.sleep(2)

        # Validate visibility and enabled state
        assert submit_button.is_displayed(), f"Submit button is not displayed: {submit_button.is_displayed()}"
        assert submit_button.is_enabled(), f"Submit button is not enabled: {submit_button.is_enabled()}"

        # Validate clickability using explicit wait
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="login-btn"]')))
        print("✓ Submit button is working properly (visible, enabled, and clickable)")

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")


# --- Test Case 4: Successful Login (Positive Test - Functionality) ---
def test_04_successful_login_positive(driver):
    """
    Validates successful login using VALID credentials
    """
    try:
        driver.get('https://www.guvi.in/sign-in/')
        # --- IMPORTANT: PLACE VALID CREDENTIALS HERE ---
        username = "" # Must be a valid email
        password = "" # Must be the corresponding valid password
        email_field = driver.find_element(By.ID, "email")
        passwd_field = driver.find_element(By.ID,"password" )
        submit_button = driver.find_element(By.XPATH, '//a[@id="login-btn"]')

        # Enter credentials and click submit
        email_field.send_keys(username)
        passwd_field.send_keys(password)
        submit_button.click()
        time.sleep(5)
        useravator = driver.find_element(By.XPATH, '//*[@id="header-container"]/div[1]/div[4]/div[2]/div/div')# Delay to allow post-login redirection/loading

        assert useravator.is_displayed(), f"Username field is not displayed: {useravator.is_displayed()}"
        print("✓ Login attempt completed with valid credentials")

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")


# --- Test Case 5: Login with Empty Credentials (Negative Test) ---
def test_05_login_with_empty_credentials(driver):
    """
    Validates login FAILURE when using empty/missing credentials.
    This is a NEGATIVE test case for login functionality.
    """
    try:
        driver.get('https://www.guvi.in/sign-in/')
        submit_button = driver.find_element(By.XPATH, '//a[@id="login-btn"]')
        submit_button.click() # Click submit without entering any text

        # Locating input fields that have received the 'is-invalid' class
        invalid_email = driver.find_element(By.XPATH, '//div[@id="emailgroup"]/input[@class="form-control is-invalid"]')
        invalid_pasword = driver.find_element(By.XPATH,'//div[@id="passwordGroup"]/input[@class="form-control is-invalid"]')

        time.sleep(5)
        # Locating an error/hint message that appears (based on provided XPath)
        forgot_password_text = driver.find_element(By.XPATH,'//div[contains(text(), "Hey, Did you forgot your password? Try again.")]')

        # Assertions for expected failures
        assert invalid_email.is_displayed(), f"Invalid Email message field is not displayed"
        assert invalid_pasword.is_displayed(), f"Invalid Password message field is not displayed"
        # The submit button should still be enabled
        assert submit_button.is_enabled(), f"Submit button not working"
        assert forgot_password_text.is_displayed(), f"Forgot password message field is not displayed"
        print("✓ Login failure test with empty credentials passed")

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")


# --- Test Case 6: Login with Incorrect Email/Password (Negative Test) ---
def test_06_login_with_invalid_email_paswrod(driver):
    """
    Validates login FAILURE when using INVALID (but formatted) credentials.
    This is a NEGATIVE test case for login functionality.
    It checks for the "Incorrect Email or Password" error message.
    """
    try:
        driver.get('https://www.guvi.in/sign-in/')

        email_field = driver.find_element(By.ID, "email")
        passwd_field = driver.find_element(By.ID,"password" )
        submit_button = driver.find_element(By.XPATH, '//a[@id="login-btn"]')

        # Enter INVALID credentials
        email_field.send_keys("sathya@tab93@gmail.com")
        passwd_field.send_keys("Satyaadffsai17@")
        submit_button.click()

        # Locating the error message for incorrect credentials (based on provided XPaths)
        incorrect_email_text = driver.find_element(By.XPATH,'//div[@id="emailgroup"]/div[contains(text(),"Incorrect Email or Password")]')
        incorrect_pasword_text = driver.find_element(By.XPATH,'//div[@id="passwordGroup"]/div[contains(text(),"Incorrect Email or Password")]')
        time.sleep(5)

        # Assertions for expected error messages
        assert incorrect_email_text.is_displayed(), f"Invalid Email message field is not displayed"
        assert incorrect_pasword_text.is_displayed(), f"Invalid Password message field is not displayed"
        print("✓ Invalid email/password combination test passed")

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")