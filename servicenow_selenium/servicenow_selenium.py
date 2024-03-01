from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, TimeoutException, NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException, JavascriptException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import webcolors
import re
import time

from servicenow_selenium.js_element import JSElement


class ServiceNowSelenium:

    # constructor
    # contains driver, url and login credentials
    def __init__(self, url, username=None, password=None):
        self.driver = webdriver.Chrome()
        self.url = url
        self.actions = ActionChains(self.driver)
        
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

    def impersonate_user(self, username=None):
        current_url = self.driver.current_url
        self.driver.get(self.url)
        if username is None:
            raise ValueError("At least one argument must be provided. username")
        user_value =  username
        user_dropdown = self.get_js_element('document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header").shadowRoot.querySelector("nav > div > div.ending-header-zone > div.polaris-header-controls > div.utility-menu.can-animate > div > now-avatar").shadowRoot.querySelector("span > span")')
        user_dropdown.click()
        impersonate_button = self.get_js_element('document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header").shadowRoot.querySelector("#userMenu > span > span:nth-child(2) > div > div.user-menu-controls > button.user-menu-button.impersonateUser.keyboard-navigatable.polaris-enabled")')
        impersonate_button.click()
        search = self.get_js_element('document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.content-area.can-animate > sn-impersonation").shadowRoot.querySelector("now-modal > div > now-typeahead").shadowRoot.querySelector("div > now-popover > div")')
        search_bar = search.find_child_elements('.now-typeahead-native-input')
        search_bar[0].set_value(user_value)
        search_bar[0].trigger_event()
        self.actions.send_keys(Keys.TAB).perform()
        self.actions.send_keys(Keys.ENTER).perform()
        time.sleep(3)
        self.actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(3)
        self.actions.send_keys(Keys.ENTER).perform()
        modal = self.get_js_element('document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.content-area.can-animate > sn-impersonation").shadowRoot.querySelector("now-modal").shadowRoot.querySelector("div > div > div")')
        impersonate_user_button = self.get_js_element('document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010").shadowRoot.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout").shadowRoot.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.content-area.can-animate > sn-impersonation").shadowRoot.querySelector("now-modal").shadowRoot.querySelector("div > div > div > div.now-modal-footer > now-button:nth-child(2)").shadowRoot.querySelector("button")')
        impersonate_user_button.click()
        self.driver.get(current_url)        
        time.sleep(5)
        # time.sleep(20)

    #impersonate user on Employee Center
    # Can take username or sys_id as arguments.
    # Will always use sys_id if both are provided.
    def impersonate_user_esc(self, username=None, user_sys_id=None):
        if username is None and user_sys_id is None:
            raise ValueError("At least one argument must be provided. username or user_sys_id")
        user_dropdown = self.driver.find_element(By.ID, "profile-dropdown")
        user_dropdown.click()
        impersonate = self.get_js_element('document.querySelector("body > div.sp-page-root.page.flex-column.sp-can-animate > section > header > div > nav > div:nth-child(1) > div > div.navbar-right.ng-scope > div > div > div > ul > li.hidden-xs.dropdown.ng-scope.open > ul > li:nth-child(2) > a")')
        impersonate.click()

        modal = self.get_js_element('document.querySelector("body > div.modal.fade.ng-isolate-scope.in > div > div")')
        modal.wait_for_element()
        # modal_dropdown = modal.find_child_elements("#select2-drop-mask")
        # print(modal_dropdown)
        # modal_dropdown[0].click()
        search_bar = self.get_js_element('document.querySelector("#s2id_autogen2_search")')
        search_bar.set_value("Test")
        time.sleep(10)
        
        # modal_search = self.get_js_element('document.querySelector("#s2id_autogen25_search")')
        # print(modal_search.get_text())
        

        # if user_sys_id is not None:
            
        # elif username is not None:

       
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
        return JSElement(self.driver, js_path, name)
            

    def convert_rgb_string_to_hex(self, rgb_string):
        # Regular expression to match both RGB and RGBA formats
        match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', rgb_string)
        if match:
            rgb_tuple = tuple(map(int, match.groups()))
            return webcolors.rgb_to_hex(rgb_tuple)
        else:
            raise ValueError("Invalid RGB/RGBA format")


