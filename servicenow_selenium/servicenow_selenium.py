from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, TimeoutException
from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ServiceNowSelenium:

    # constructor
    # contains driver, url and login credentials
    def __init__(self, url, username, password):
        self.driver = webdriver.Chrome()
        self.url = url
        self.username = username
        self.password = password


    # Login function, initializes driver and logs in based on values provided
    def login(self):
        # Initialize 
        self.driver.maximize_window() # Full screen window
        self.driver.get(self.url) # Navigate to url given by constructor
        self.accept_alert() # Catch any alerts

           

        # Login using username/password
        username_field = self.driver.find_element(By.NAME, 'user_name')
        username_field.send_keys(self.username)

        password_field = self.driver.find_element(By.NAME, 'user_password')
        password_field.send_keys(self.password)

        login_button = self.driver.find_element(By.ID, 'sysverb_login')
        login_button.click()

       
    # Logout and quit driver function
    def logout(self):

        user_menu_path = '''document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot
        .querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot
        .querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header").shadowRoot
        .querySelector("#userMenu")
        '''

        self.click_shadow_element("user menu button", user_menu_path)

        logout_path = '''document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot
        .querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot
        .querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header").shadowRoot
        .querySelector("#userMenu > span > span:nth-child(2) > div > div.user-menu-footer > button > div")
        '''

        self.click_shadow_element("logout button", logout_path)
        

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

