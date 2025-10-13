from __future__ import annotations
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def build_webdriver(browser: str = "chrome", headless: bool = True, pageload_timeout: int = 60, implicit_wait: int = 0) -> webdriver.Remote:
    browser = browser.lower()
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        caps = DesiredCapabilities.CHROME.copy()
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        caps = DesiredCapabilities.FIREFOX.copy()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options, desired_capabilities=caps)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.set_page_load_timeout(pageload_timeout)
    if implicit_wait:
        driver.implicitly_wait(implicit_wait)
    return driver
