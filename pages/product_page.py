"""Product page object model for Profitero website."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List, Dict


class ProductPage(BasePage):
    """Product page object model."""
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h1")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".product-description, .description")
    PRODUCT_FEATURES = (By.CSS_SELECTOR, ".feature-list li, .features li")
    PRODUCT_BENEFITS = (By.CSS_SELECTOR, ".benefit-list li, .benefits li")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product-image, .hero-image img")
    REQUEST_DEMO_BUTTON = (By.LINK_TEXT, "Request a demo")
    LEARN_MORE_BUTTON = (By.LINK_TEXT, "Learn more")
    
    # Breadcrumb navigation
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")
    BREADCRUMB_LINKS = (By.CSS_SELECTOR, ".breadcrumb a")
    
    # Related products/services
    RELATED_PRODUCTS = (By.CSS_SELECTOR, ".related-products")
    RELATED_PRODUCT_LINKS = (By.CSS_SELECTOR, ".related-products a")
    
    # Video/Demo section
    VIDEO_SECTION = (By.CSS_SELECTOR, ".video-section")
    PLAY_VIDEO_BUTTON = (By.CSS_SELECTOR, ".play-button, .video-play")
    
    # Testimonials/Case studies
    TESTIMONIALS = (By.CSS_SELECTOR, ".testimonial")
    CASE_STUDIES = (By.CSS_SELECTOR, ".case-study")
    
    def __init__(self, driver):
        """Initialize product page."""
        super().__init__(driver)
    
    def open_product_page(self, product_url: str):
        """Open specific product page."""
        self.open(product_url)
        return self
    
    def get_product_title(self) -> str:
        """Get product title."""
        return self.get_text(self.PAGE_TITLE)
    
    def get_product_description(self) -> str:
        """Get product description."""
        return self.get_text(self.PRODUCT_DESCRIPTION)
    
    def get_product_features(self) -> List[str]:
        """Get list of product features."""
        features = []
        feature_elements = self.find_elements(self.PRODUCT_FEATURES)
        
        for element in feature_elements:
            text = element.text.strip()
            if text:
                features.append(text)
        
        return features
    
    def get_product_benefits(self) -> List[str]:
        """Get list of product benefits."""
        benefits = []
        benefit_elements = self.find_elements(self.PRODUCT_BENEFITS)
        
        for element in benefit_elements:
            text = element.text.strip()
            if text:
                benefits.append(text)
        
        return benefits
    
    def get_product_images(self) -> List[Dict[str, str]]:
        """Get product images."""
        images = []
        image_elements = self.find_elements(self.PRODUCT_IMAGES)
        
        for element in image_elements:
            src = element.get_attribute("src")
            alt = element.get_attribute("alt")
            if src:
                images.append({"src": src, "alt": alt or ""})
        
        return images
    
    def click_request_demo(self):
        """Click request demo button."""
        return self.click_element(self.REQUEST_DEMO_BUTTON)
    
    def click_learn_more(self):
        """Click learn more button."""
        return self.click_element(self.LEARN_MORE_BUTTON)
    
    def is_request_demo_button_visible(self) -> bool:
        """Check if request demo button is visible."""
        return self.is_element_visible(self.REQUEST_DEMO_BUTTON)
    
    def get_breadcrumb_navigation(self) -> List[Dict[str, str]]:
        """Get breadcrumb navigation."""
        breadcrumbs = []
        breadcrumb_elements = self.find_elements(self.BREADCRUMB_LINKS)
        
        for element in breadcrumb_elements:
            text = element.text.strip()
            href = element.get_attribute("href")
            if text:
                breadcrumbs.append({"text": text, "href": href or ""})
        
        return breadcrumbs
    
    def get_related_products(self) -> List[Dict[str, str]]:
        """Get related products."""
        products = []
        product_elements = self.find_elements(self.RELATED_PRODUCT_LINKS)
        
        for element in product_elements:
            text = element.text.strip()
            href = element.get_attribute("href")
            if text and href:
                products.append({"text": text, "href": href})
        
        return products
    
    def is_video_section_present(self) -> bool:
        """Check if video section is present."""
        return self.is_element_present(self.VIDEO_SECTION)
    
    def play_product_video(self):
        """Play product video."""
        if self.is_element_visible(self.PLAY_VIDEO_BUTTON):
            return self.click_element(self.PLAY_VIDEO_BUTTON)
        return False
    
    def get_testimonials(self) -> List[str]:
        """Get testimonials."""
        testimonials = []
        testimonial_elements = self.find_elements(self.TESTIMONIALS)
        
        for element in testimonial_elements:
            text = element.text.strip()
            if text:
                testimonials.append(text)
        
        return testimonials
    
    def get_case_studies(self) -> List[str]:
        """Get case studies."""
        case_studies = []
        case_study_elements = self.find_elements(self.CASE_STUDIES)
        
        for element in case_study_elements:
            text = element.text.strip()
            if text:
                case_studies.append(text)
        
        return case_studies
    
    def scroll_to_features_section(self):
        """Scroll to features section."""
        if self.is_element_present(self.PRODUCT_FEATURES):
            self.scroll_to_element(self.PRODUCT_FEATURES)
    
    def scroll_to_video_section(self):
        """Scroll to video section."""
        if self.is_element_present(self.VIDEO_SECTION):
            self.scroll_to_element(self.VIDEO_SECTION)
    
    def verify_product_page_load(self) -> bool:
        """Verify product page has loaded correctly."""
        return (
            bool(self.get_product_title()) and
            self.is_request_demo_button_visible()
        )
    
    def extract_product_data(self) -> Dict:
        """Extract all product data."""
        return {
            "title": self.get_product_title(),
            "description": self.get_product_description(),
            "features": self.get_product_features(),
            "benefits": self.get_product_benefits(),
            "images": self.get_product_images(),
            "breadcrumbs": self.get_breadcrumb_navigation(),
            "related_products": self.get_related_products(),
            "testimonials": self.get_testimonials(),
            "case_studies": self.get_case_studies(),
            "has_video": self.is_video_section_present(),
            "has_demo_button": self.is_request_demo_button_visible()
        }