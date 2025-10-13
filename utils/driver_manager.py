"""WebDriver manager for Selenium tests."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import os
import random
from typing import Optional
from utils.config_reader import config


class DriverManager:
    """Manage WebDriver instances for different browsers."""
    
    def __init__(self):
        """Initialize driver manager."""
        self.driver: Optional[webdriver.Remote] = None
        self.browser = config.get_browser().lower()
        self.headless = config.is_headless()
        self.window_size = config.get_window_size()
        self.timeout = config.get_timeout()
    
    def get_chrome_options(self) -> ChromeOptions:
        """Get Chrome browser options."""
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
        
        # Random user agent for web scraping
        user_agents = config.get('scraping.user_agents', [])
        if user_agents:
            user_agent = random.choice(user_agents)
            options.add_argument(f'--user-agent={user_agent}')
        
        # Additional preferences
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "geolocation": 2,
                "media_stream": 2,
            }
        }
        options.add_experimental_option("prefs", prefs)
        
        return options
    
    def get_firefox_options(self) -> FirefoxOptions:
        """Get Firefox browser options."""
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Set preferences
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("geo.enabled", False)
        
        return options
    
    def get_edge_options(self) -> EdgeOptions:
        """Get Edge browser options."""
        options = EdgeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        
        return options
    
    def create_driver(self) -> webdriver.Remote:
        """Create and return WebDriver instance."""
        try:
            if self.browser == 'chrome':
                service = ChromeService(ChromeDriverManager().install())
                options = self.get_chrome_options()
                self.driver = webdriver.Chrome(service=service, options=options)
            
            elif self.browser == 'firefox':
                service = FirefoxService(GeckoDriverManager().install())
                options = self.get_firefox_options()
                self.driver = webdriver.Firefox(service=service, options=options)
            
            elif self.browser == 'edge':
                service = EdgeService(EdgeChromiumDriverManager().install())
                options = self.get_edge_options()
                self.driver = webdriver.Edge(service=service, options=options)
            
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")
            
            # Set timeouts
            self.driver.implicitly_wait(config.get('implicit_wait', 10))
            self.driver.set_page_load_timeout(self.timeout)
            
            # Maximize window if not headless
            if not self.headless:
                self.driver.maximize_window()
            
            return self.driver
        
        except Exception as e:
            raise RuntimeError(f"Failed to create WebDriver: {str(e)}")
    
    def quit_driver(self):
        """Quit the WebDriver instance."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {e}")
            finally:
                self.driver = None
    
    def get_driver(self) -> webdriver.Remote:
        """Get current driver instance or create new one."""
        if not self.driver:
            self.driver = self.create_driver()
        return self.driver