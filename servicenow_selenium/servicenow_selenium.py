from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, TimeoutException
from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webcolors
import re
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


    # Method to get a JSElement
    def get_js_element(self, js_path, name=""):
        return self.JSElement(self.driver, js_path, name)


    class JSElement:
        def __init__(self, driver, js_path, name=""):
            self.driver = driver
            self.js_path = js_path
            self.name = name  # Name of the element for error reporting

        # JS queries the element then checks for it's existence.
        def is_present(self):
            try:
                element = self.driver.execute_script(f"return {self.js_path}")
                return element is not None
            except Exception:
                pass
            try:
                outer_html = self.driver.execute_script(f"return {self.js_path}.outerHTML;")
                return bool(outer_html)
            except Exception:
                return False
            
        # JS queries the element to determine if it's visible on the screen
        def is_visible(self, wait_time=10):
            try:
                WebDriverWait(self.driver, wait_time).until(lambda x: self.is_present())
                return self.driver.execute_script(f"return {self.js_path}.offsetParent !== null")
            except Exception as e:
                raise Exception(f"Error checking visibility of element {self.name}: {str(e)}")
            
        def hover(self):
            try:
                hover_script = f"const event = new MouseEvent('mouseover', {{bubbles: true}}); {self.js_path}.dispatchEvent(event);"
                self.driver.execute_script(hover_script)
            except Exception as e:
                raise Exception(f"Error simulating hover on element {self.name}: {str(e)}")

        # Click the element. Queries until it's found and then clicked.
        def click(self, wait_time=10):
            try:
                WebDriverWait(self.driver, wait_time).until(lambda x: self.is_present())
                self.driver.execute_script(f"return {self.js_path}.click()")
            except (TimeoutException, ElementNotVisibleException, ElementNotInteractableException) as e:
                raise Exception(f"The element{self.name} was not found or not interactable. Additional info: {str(e)}")

        def get_outer_html(self, wait_time=10):
            try:
                WebDriverWait(self.driver, wait_time).until(lambda x: self.is_present())
                return self.driver.execute_script(f"return {self.js_path}.outerHTML")
            except Exception as e:
                raise Exception(f"Error getting text from element {self.name}: {str(e)}")
        
        # Retrieves html of the element.
        def get_text(self, wait_time=10):
            try:
                WebDriverWait(self.driver, wait_time).until(lambda x: self.is_present())
                return self.driver.execute_script(f"return {self.js_path}.textContent || {self.js_path}.innerText")
            except Exception as e:
                raise Exception(f"Error getting text from element {self.name}: {str(e)}")
            
        # Take css property as in input.
        def value_of_css_property(self, css_property_name, wait_time=10):
            try:
                WebDriverWait(self.driver, wait_time).until(lambda x: self.is_present())
                return self.driver.execute_script(f"return window.getComputedStyle({self.js_path}).getPropertyValue('{css_property_name}');")
            except Exception as e:
                raise Exception(f"Error getting CSS property from element  {self.name}: {str(e)}")
            
        def get_pseudo_element_css_property(self, pseudo_element, css_property_name, wait_time=10):
            try:
                WebDriverWait(self.driver,wait_time).until(lambda x: self.is_present())
                script = f"return window.getComputedStyle({self.js_path}, '{pseudo_element}').getPropertyValue('{css_property_name}');"
                return self.driver.execute_script(script)
            except Exception as e:
                raise Exception(f"Error getting CSS property '{css_property_name}' from pseudo-element '{pseudo_element}' for {self.name}: {str(e)}")
            
    def convert_rgb_string_to_hex(self, rgb_string):
        match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', rgb_string)
        if match:
            rgb_tuple = tuple(map(int, match.groups()))
            return webcolors.rgb_to_hex(rgb_tuple)
        else:
            raise ValueError("Invalid RGB format")


