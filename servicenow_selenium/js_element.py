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

class JSElement:
        def __init__(self, driver, js_path, name=""):
            self.driver = driver
            self.js_path = js_path
            self.name = name  # Name of the element for error reporting

        # Execute wrapper for loggin errors
        def execute_script(self, script):
            try:
                return self.driver.execute_script(script)
            except JavascriptException as e:
                print(f"JavascriptException: {e}")
            

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
            
        def wait_for_element(self, timeout=10):
            try:
                WebDriverWait(self.driver,timeout).until(lambda x: self.is_present())
                return True
            except TimeoutException:
                return False

            
        # JS queries the element to determine if it's visible on the screen
        def is_visible(self):
            try:
                self.wait_for_element()
                return self.execute_script(f"return {self.js_path}.offsetParent !== null")
            except Exception as e:
                raise Exception(f"Error checking visibility of element {self.name}: {str(e)}")
            
        # Dispatch and event to get any event listeners to handle things.
        def trigger_event(self):
            declare_event = """var event = new Event('input', {
                                'bubbles': true,
                                'cancelable':true

                            });
                            """
            try:
                self.wait_for_element()
                return self.execute_script(f"{declare_event} return {self.js_path}.dispatchEvent(event)")
            except Exception as e:
                raise Exception(f"Error dispatching event onto element {self.name}: {str(e)}")
            
            
        def hover(self):
            try:
                self.wait_for_element()
                hover_script = f"const event = new MouseEvent('mouseover', {{bubbles: true}}); {self.js_path}.dispatchEvent(event);"
                self.execute_script(hover_script)
            except Exception as e:
                raise Exception(f"Error simulating hover on element {self.name}: {str(e)}")

        # Click the element. Queries until it's found and then clicked.
        def click(self):
            try:
                self.wait_for_element()
                self.execute_script(f"return {self.js_path}.click()")
            except (TimeoutException, ElementNotVisibleException, ElementNotInteractableException) as e:
                raise Exception(f"The element{self.name} was not found or not interactable. Additional info: {str(e)}")
            
        def set_value(self,value):
            try:
                self.wait_for_element()
                self.execute_script(f"return {self.js_path}.value = '{value}'")
            except (TimeoutException, ElementNotVisibleException, ElementNotInteractableException) as e:
                raise Exception(f"Could not update element{self.name} withe the following value: {value}. Additional info: {str(e)}")
            
        def get_outer_html(self):
            try:
                self.wait_for_element()
                return str(self.execute_script(f"return {self.js_path}.outerHTML"))
            except Exception as e:
                raise Exception(f"Error getting text from element {self.name}: {str(e)}")
        
        # Retrieves html of the element.
        def get_text(self):
            try:
                self.wait_for_element()
                return str(self.execute_script(f"return {self.js_path}.textContent || {self.js_path}.innerText"))
            except Exception as e:
                raise Exception(f"Error getting text from element {self.name}: {str(e)}")
            
        def get_attribute(self, attribute_name):
            try:
                self.wait_for_element()
                return str(self.execute_script(f"return {self.js_path}.getAttribute('{attribute_name}');"))
            except Exception as e:
                raise Exception(f"Error getting attribute '{attribute_name}' from element  {self.name}: {str(e)}")
       
        # Take css property as in input.
        def value_of_css_property(self, css_property_name):
            try:
                self.wait_for_element()
                return self.execute_script(f"return window.getComputedStyle({self.js_path}).getPropertyValue('{css_property_name}');")
            except Exception as e:
                raise Exception(f"Error getting CSS property '{css_property_name}' from element  {self.name}: {str(e)}")
            
        def get_pseudo_element_css_property(self, pseudo_element, css_property_name):
            try:
                self.wait_for_element()
                script = f"return window.getComputedStyle({self.js_path}, '{pseudo_element}').getPropertyValue('{css_property_name}');"
                return self.execute_script(script)
            except Exception as e:
                raise Exception(f"Error getting CSS property '{css_property_name}' from pseudo-element '{pseudo_element}' for {self.name}: {str(e)}")
            
        def find_child_elements(self, child_selector):
            try:
                self.wait_for_element()
                children_count = self.execute_script(f"return {self.js_path}.querySelectorAll('{child_selector}').length;")
                return [self.__class__(self.driver, f"({self.js_path}.querySelectorAll('{child_selector}'))[{i}]", f"{self.name}_child_{i}") for i in range(children_count)]
            except Exception as e:
                raise Exception(f"Could not find any child elements inside {self.name} under the name of {child_selector}: {str(e)}")
            
