"""Home page object model for Profitero website."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List, Dict


class HomePage(BasePage):
    """Home page object model."""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, ".navbar_logo")
    MAIN_NAVIGATION = (By.CSS_SELECTOR, ".navbar_menu")
    PRODUCTS_DROPDOWN = (By.CSS_SELECTOR, "[data-w-id*='dropdown']")
    PRODUCTS_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, ".navbar_dropdown-toggle")
    HERO_SECTION = (By.CSS_SELECTOR, ".hero-section, .section")
    HERO_TITLE = (By.CSS_SELECTOR, "h1")
    HERO_DESCRIPTION = (By.CSS_SELECTOR, ".hero-description, .hero-text")
    CTA_BUTTON = (By.CSS_SELECTOR, ".button, .cta-button")
    REQUEST_DEMO_BUTTON = (By.LINK_TEXT, "Request a demo")
    
    # Product links
    DIGITAL_SHELF_LINK = (By.LINK_TEXT, "Digital Shelf")
    SALES_SHARE_LINK = (By.LINK_TEXT, "Sales & Share")
    CONTENT_OPTIMIZER_LINK = (By.LINK_TEXT, "Content Optimizer")
    SHELF_INTELLIGENT_MEDIA_LINK = (By.LINK_TEXT, "Shelf Intelligent Media")
    AUTOPILOT_LINK = (By.LINK_TEXT, "Autopilot")
    
    # Services links
    MEDIA_SERVICES_LINK = (By.LINK_TEXT, "Media")
    CONTENT_SERVICES_LINK = (By.LINK_TEXT, "Content")
    OPERATIONS_SERVICES_LINK = (By.LINK_TEXT, "Operations")
    STRATEGY_INSIGHTS_LINK = (By.LINK_TEXT, "Strategy & Insights")
    
    # Footer elements
    FOOTER = (By.CSS_SELECTOR, ".footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, ".footer-link-block")
    SOCIAL_LINKS = (By.CSS_SELECTOR, ".footer-social-icon")
    
    # Top navigation
    TOP_NAV_ABOUT = (By.LINK_TEXT, "About")
    TOP_NAV_CAREERS = (By.LINK_TEXT, "Careers")
    TOP_NAV_CONTACT = (By.LINK_TEXT, "Contact")
    
    def __init__(self, driver):
        """Initialize home page."""
        super().__init__(driver)
        self.page_url = "/"
    
    def open_homepage(self):
        """Open homepage."""
        self.open(self.page_url)
        return self
    
    def is_logo_displayed(self) -> bool:
        """Check if logo is displayed."""
        return self.is_element_visible(self.LOGO)
    
    def click_logo(self):
        """Click on logo."""
        return self.click_element(self.LOGO)
    
    def get_page_title(self) -> str:
        """Get page title."""
        return self.get_title()
    
    def get_hero_title(self) -> str:
        """Get hero section title."""
        return self.get_text(self.HERO_TITLE)
    
    def get_hero_description(self) -> str:
        """Get hero section description."""
        return self.get_text(self.HERO_DESCRIPTION)
    
    def click_request_demo(self):
        """Click request demo button."""
        return self.click_element(self.REQUEST_DEMO_BUTTON)
    
    def hover_over_products_menu(self):
        """Hover over products dropdown menu."""
        return self.hover_over_element(self.PRODUCTS_DROPDOWN_TOGGLE)
    
    def click_products_dropdown(self):
        """Click products dropdown."""
        return self.click_element(self.PRODUCTS_DROPDOWN_TOGGLE)
    
    def navigate_to_digital_shelf(self):
        """Navigate to Digital Shelf product page."""
        if self.hover_over_products_menu():
            return self.click_element(self.DIGITAL_SHELF_LINK)
        return False
    
    def navigate_to_sales_share(self):
        """Navigate to Sales & Share product page."""
        if self.hover_over_products_menu():
            return self.click_element(self.SALES_SHARE_LINK)
        return False
    
    def navigate_to_content_optimizer(self):
        """Navigate to Content Optimizer product page."""
        if self.hover_over_products_menu():
            return self.click_element(self.CONTENT_OPTIMIZER_LINK)
        return False
    
    def navigate_to_shelf_intelligent_media(self):
        """Navigate to Shelf Intelligent Media product page."""
        if self.hover_over_products_menu():
            return self.click_element(self.SHELF_INTELLIGENT_MEDIA_LINK)
        return False
    
    def navigate_to_autopilot(self):
        """Navigate to Autopilot product page."""
        if self.hover_over_products_menu():
            return self.click_element(self.AUTOPILOT_LINK)
        return False
    
    def navigate_to_about(self):
        """Navigate to About page."""
        return self.click_element(self.TOP_NAV_ABOUT)
    
    def navigate_to_careers(self):
        """Navigate to Careers page."""
        return self.click_element(self.TOP_NAV_CAREERS)
    
    def navigate_to_contact(self):
        """Navigate to Contact page."""
        return self.click_element(self.TOP_NAV_CONTACT)
    
    def get_all_navigation_links(self) -> List[Dict[str, str]]:
        """Get all navigation links."""
        links = []
        nav_elements = self.find_elements((By.CSS_SELECTOR, ".navbar_menu a"))
        
        for element in nav_elements:
            href = element.get_attribute("href")
            text = element.text.strip()
            if href and text:
                links.append({"text": text, "href": href})
        
        return links
    
    def get_all_footer_links(self) -> List[Dict[str, str]]:
        """Get all footer links."""
        links = []
        footer_elements = self.find_elements(self.FOOTER_LINKS)
        
        for element in footer_elements:
            href = element.get_attribute("href")
            text = element.text.strip()
            if href and text:
                links.append({"text": text, "href": href})
        
        return links
    
    def get_social_media_links(self) -> List[str]:
        """Get social media links."""
        links = []
        social_elements = self.find_elements(self.SOCIAL_LINKS)
        
        for element in social_elements:
            # Get parent link element
            parent_link = element.find_element(By.XPATH, "..")
            href = parent_link.get_attribute("href")
            if href:
                links.append(href)
        
        return links
    
    def is_main_navigation_visible(self) -> bool:
        """Check if main navigation is visible."""
        return self.is_element_visible(self.MAIN_NAVIGATION)
    
    def is_hero_section_visible(self) -> bool:
        """Check if hero section is visible."""
        return self.is_element_visible(self.HERO_SECTION)
    
    def is_footer_visible(self) -> bool:
        """Check if footer is visible."""
        return self.is_element_visible(self.FOOTER)
    
    def scroll_to_footer(self):
        """Scroll to footer."""
        self.scroll_to_element(self.FOOTER)
    
    def get_cta_buttons(self) -> List[Dict[str, str]]:
        """Get all CTA buttons."""
        buttons = []
        cta_elements = self.find_elements(self.CTA_BUTTON)
        
        for element in cta_elements:
            text = element.text.strip()
            href = element.get_attribute("href")
            if text:
                buttons.append({"text": text, "href": href or ""})
        
        return buttons
    
    def verify_page_load(self) -> bool:
        """Verify page has loaded correctly."""
        return (
            self.is_logo_displayed() and
            self.is_main_navigation_visible() and
            self.is_hero_section_visible()
        )
    
    def get_page_performance_metrics(self) -> Dict:
        """Get page performance metrics."""
        return self.helpers.get_page_performance_metrics()
    
    def check_for_console_errors(self) -> List:
        """Check for JavaScript console errors."""
        return self.helpers.check_console_errors()