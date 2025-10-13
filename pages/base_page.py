"""Base page class for Page Object Model."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config_reader import config
from utils.test_helpers import TestHelpers
import logging


class BasePage:
    """Base page class with common functionality."""
    
    def __init__(self, driver):
        """Initialize base page."""
        self.driver = driver
        self.wait = WebDriverWait(driver, config.get_timeout())
        self.helpers = TestHelpers(driver)
        self.logger = logging.getLogger(__name__)
        self.base_url = config.get_base_url()
    
    def open(self, url: str = None):
        """Open page URL."""
        if url:
            full_url = url if url.startswith('http') else f"{self.base_url}{url}"
        else:
            full_url = self.base_url
        
        self.driver.get(full_url)
        self.logger.info(f"Opened page: {full_url}")
    
    def get_title(self) -> str:
        """Get page title."""
        return self.driver.title
    
    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
    
    def wait_for_element(self, locator: tuple, timeout: int = None) -> bool:
        """Wait for element to be present."""
        timeout = timeout or config.get_timeout()
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.warning(f"Element not found: {locator}")
            return False
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """Wait for element to be visible."""
        timeout = timeout or config.get_timeout()
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.warning(f"Element not visible: {locator}")
            return False
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> bool:
        """Wait for element to be clickable."""
        timeout = timeout or config.get_timeout()
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            self.logger.warning(f"Element not clickable: {locator}")
            return False
    
    def find_element(self, locator: tuple):
        """Find element by locator."""
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            self.logger.error(f"Element not found: {locator}")
            return None
    
    def find_elements(self, locator: tuple):
        """Find elements by locator."""
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            self.logger.error(f"Elements not found: {locator}")
            return []
    
    def click_element(self, locator: tuple):
        """Click element."""
        if self.wait_for_element_clickable(locator):
            element = self.find_element(locator)
            if element:
                try:
                    element.click()
                    self.logger.info(f"Clicked element: {locator}")
                    return True
                except Exception as e:
                    self.logger.error(f"Error clicking element {locator}: {str(e)}")
                    return False
        return False
    
    def enter_text(self, locator: tuple, text: str):
        """Enter text in element."""
        if self.wait_for_element_visible(locator):
            element = self.find_element(locator)
            if element:
                try:
                    element.clear()
                    element.send_keys(text)
                    self.logger.info(f"Entered text '{text}' in element: {locator}")
                    return True
                except Exception as e:
                    self.logger.error(f"Error entering text in element {locator}: {str(e)}")
                    return False
        return False
    
    def get_text(self, locator: tuple) -> str:
        """Get text from element."""
        if self.wait_for_element_visible(locator):
            element = self.find_element(locator)
            if element:
                return element.text
        return ""
    
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Get attribute value from element."""
        if self.wait_for_element(locator):
            element = self.find_element(locator)
            if element:
                return element.get_attribute(attribute) or ""
        return ""
    
    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: tuple) -> bool:
        """Check if element is visible."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, locator: tuple):
        """Scroll to element."""
        element = self.find_element(locator)
        if element:
            self.helpers.scroll_to_element(element)
    
    def hover_over_element(self, locator: tuple):
        """Hover over element."""
        if self.wait_for_element_visible(locator):
            element = self.find_element(locator)
            if element:
                try:
                    ActionChains(self.driver).move_to_element(element).perform()
                    self.logger.info(f"Hovered over element: {locator}")
                    return True
                except Exception as e:
                    self.logger.error(f"Error hovering over element {locator}: {str(e)}")
                    return False
        return False
    
    def take_screenshot(self, name: str = None) -> str:
        """Take screenshot."""
        return self.helpers.take_screenshot(name)
    
    def refresh_page(self):
        """Refresh current page."""
        self.driver.refresh()
        self.logger.info("Page refreshed")
    
    def go_back(self):
        """Go back to previous page."""
        self.driver.back()
        self.logger.info("Navigated back")
    
    def switch_to_new_tab(self):
        """Switch to new tab."""
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    def close_current_tab(self):
        """Close current tab."""
        self.driver.close()
        if len(self.driver.window_handles) > 0:
            self.driver.switch_to.window(self.driver.window_handles[0])
    
    def accept_alert(self):
        """Accept alert dialog."""
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            self.logger.info("Alert accepted")
            return True
        except Exception as e:
            self.logger.error(f"Error accepting alert: {str(e)}")
            return False
    
    def dismiss_alert(self):
        """Dismiss alert dialog."""
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            self.logger.info("Alert dismissed")
            return True
        except Exception as e:
            self.logger.error(f"Error dismissing alert: {str(e)}")
            return False