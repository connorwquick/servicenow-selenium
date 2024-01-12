# ServiceNow Selenium Wrapper

A simple selenium wrapper designed for interaction with ServiceNow. This package simplifies logging in, managing alerts, and interacting with shadow elements within the ServiceNow environment.

## Installation

To install the package, use pip:

```bash
pip install servicenow-selenium
```

## Usage

Initialize the ServiceNowSelenium class by providing the URL, username, and password:

```python
from servicenow_selenium import ServiceNowSelenium

selenium_wrapper = ServiceNowSelenium(url="YOUR_SERVICENOW_URL", username="YOUR_USERNAME", password="YOUR_PASSWORD")
```

### Key Features:

1. **Login**:
   Easily log into ServiceNow:

   ```python
   selenium_wrapper.login()
   ```
2. **Logout**:
   Log out and quit the driver:

   ```python
   selenium_wrapper.logout(user_menu_path="JS_PATH_HERE", logout_path="JS_PATH_HERE")
   ```
   ```python
   selenium_wrapper.logout_endpoint()
   ```
3. **Interact with Shadow DOM Elements**:
   Click shadow elements using JS path:

   ```python
   js_element = selenium_wrapper.get_js_element(js_path="JS_PATH_HERE")
   js_element.click()
   ```
   Note: The provided JS path must contain "return" to correctly fetch the element. For instance, `return document.querySelector(...)`
4. **Utlize the JSElement class to interact with shadow dom elements**:
   Determine if an element is present using its JS path:

   ```python
   color = js_element.value_of_css_property("color")
   children = js_element.find_child_elements("div.className")
   ```
