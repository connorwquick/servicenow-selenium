from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, TimeoutException
from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

class ServiceNowSelenium:

    # constructor
    # contains driver, url and login credentials
    def __init__(self, url, username=None, password=None):
        self.driver = webdriver.Chrome()
        self.url = url
        
        if username is None:
            self.username = input("Please enter your username: ")
        else:
            self.username = username
        
        if password is None:
            self.password = input("Please enter your password: ")
        else:
            self.password = password

    # Login function, initializes driver and logs in based on values provided
    def login(self):
        # Initialize 
        self.driver.get(self.url) # Navigate to url given by constructor
        self.accept_alert() # Catch any alerts

           

        # Login using username/password
        username_field = self.driver.find_element(By.NAME, 'user_name')
        username_field.send_keys(self.username)

        password_field = self.driver.find_element(By.NAME, 'user_password')
        password_field.send_keys(self.password)

        login_button = self.driver.find_element(By.ID, 'sysverb_login')
        login_button.click()

        # Accept and prompt for MFA if necessary
        self.accept_mfa()
       
    # Logout and quit driver function
    def logout(self, user_menu_path, logout_path):

        self.click_shadow_element("user menu button", user_menu_path)
        self.click_shadow_element("logout button", logout_path)

        self.driver.quit()

    # Logout via endpoint
    def logout_endpoint(self):
        self.driver.get(f"{self.url}/logout.do")
        self.driver.quit()


    # Check if an element is present using JS path.
    # Particularly useful for shadow DOM elements
    def is_element_present(self, js_path):
        # Attempt to return the element as is
        try:
            element = self.driver.execute_script(f"return {js_path}")
            return element is not None
        except Exception:
            pass
        # Attempt to detect outerHTML as second measure
        try:
            # Extract the outerHTML of the element
            outer_html = self.driver.execute_script(f"return {js_path}.outerHTML;")
            
            # Check if the outerHTML is not null or empty
            if outer_html:
                return True
        except Exception:
            return False

    # used to click shadow elements w/ js path.
    # uses javascript to allow for explicit waits        
    def click_shadow_element(self, errorName, js_path, wait_time = 10):
        try:
            # Try to poll for element presence
            WebDriverWait(self.driver, wait_time).until(lambda x: self.is_element_present(js_path))
            self.driver.execute_script(f"return {js_path}.click()")

        except (TimeoutException, ElementNotVisibleException, ElementNotInteractableException) as e:
            # If nothing works, then the element might not be present or interactable
            raise Exception(f"The {errorName} button was not found. Additional info: {str(e)}")


    # Wait and accept alerts as they come
    def accept_alert(self):
        try:
            WebDriverWait(self.driver, .5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Alert accepted")
        except (NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException):
            pass

    # Prompt user to input Multi-Factor Authentication
    def accept_mfa(self):
        # Check if the MFA options div is present
        mfa_div_elements = self.driver.find_elements(By.ID, "mfa_options")
        if mfa_div_elements:
            mfa_div = mfa_div_elements[0]
            if mfa_div:
                # Click the continue button
                continue_button = self.driver.find_element(By.ID, "continue")
                continue_button.click()
                
                # Prompt the user for the MFA code
                mfa_code = input("Please enter your MFA code: ")
                
                # Input the MFA code into the provided field
                mfa_input = self.driver.find_element(By.ID, "txtResponse")
                mfa_input.send_keys(mfa_code)
                
                # Click the validate MFA code button
                validate_button = self.driver.find_element(By.ID, "sysverb_validate_mfa_code")
                validate_button.click()

    def run_test_modal(self):
        try:
            WebDriverWait(self.driver, .5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Running Test")
        except (NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException):
            pass
    

    def run_atf(self, test_suite_sys_id, run_test_path):
        # Define the endpoint URL for the ATF test
        atf_url = f"{self.url}sys_atf_test.do?sys_id={test_suite_sys_id}"
        self.driver.get(atf_url)

        run_test_button = self.driver.find_element(By.ID, 'd69ab3705b2212006f23efe5f0f91ada_bottom')
        run_test_button.click()
        run_modal_test_button = self.driver.find_element(By.ID, 'run_button')
        run_modal_test_button.click()
        # self.run_test_modal()




