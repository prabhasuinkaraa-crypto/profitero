from __future__ import annotations
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip('/')

    def open(self, path: str = "/") -> None:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        self.driver.get(url)

    def click(self, by: By, locator: str, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        ).click()

    def type(self, by: By, locator: str, text: str, timeout: int = 15) -> None:
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
        element.clear()
        element.send_keys(text)

    def wait_visible(self, by: By, locator: str, timeout: int = 15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def get_text(self, by: By, locator: str, timeout: int = 15) -> str:
        element = self.wait_visible(by, locator, timeout)
        return element.text

    def exists(self, by: By, locator: str, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return True
        except Exception:
            return False
