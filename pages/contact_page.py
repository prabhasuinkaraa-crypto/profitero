"""Contact page object model for Profitero website."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Dict, List


class ContactPage(BasePage):
    """Contact page object model."""
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h1")
    CONTACT_FORM = (By.CSS_SELECTOR, ".contact-form, form")
    
    # Form fields
    FIRST_NAME_FIELD = (By.CSS_SELECTOR, "input[name*='first'], input[name*='fname'], #first-name")
    LAST_NAME_FIELD = (By.CSS_SELECTOR, "input[name*='last'], input[name*='lname'], #last-name")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='email'], input[name*='email'], #email")
    COMPANY_FIELD = (By.CSS_SELECTOR, "input[name*='company'], #company")
    PHONE_FIELD = (By.CSS_SELECTOR, "input[type='tel'], input[name*='phone'], #phone")
    MESSAGE_FIELD = (By.CSS_SELECTOR, "textarea[name*='message'], #message")
    SUBJECT_FIELD = (By.CSS_SELECTOR, "input[name*='subject'], #subject")
    
    # Dropdown fields
    COUNTRY_DROPDOWN = (By.CSS_SELECTOR, "select[name*='country'], #country")
    INDUSTRY_DROPDOWN = (By.CSS_SELECTOR, "select[name*='industry'], #industry")
    COMPANY_SIZE_DROPDOWN = (By.CSS_SELECTOR, "select[name*='size'], #company-size")
    
    # Buttons
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[type='submit'], button[type='submit'], .submit-button")
    RESET_BUTTON = (By.CSS_SELECTOR, "input[type='reset'], .reset-button")
    
    # Contact information
    CONTACT_INFO_SECTION = (By.CSS_SELECTOR, ".contact-info")
    EMAIL_ADDRESS = (By.CSS_SELECTOR, ".email-address")
    PHONE_NUMBER = (By.CSS_SELECTOR, ".phone-number")
    ADDRESS = (By.CSS_SELECTOR, ".address")
    
    # Social media links
    SOCIAL_LINKS = (By.CSS_SELECTOR, ".social-links a")
    
    # Success/Error messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message, .alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-error")
    
    # Map section
    MAP_SECTION = (By.CSS_SELECTOR, ".map-section, #map")
    
    def __init__(self, driver):
        """Initialize contact page."""
        super().__init__(driver)
        self.page_url = "/contact"
    
    def open_contact_page(self):
        """Open contact page."""
        self.open(self.page_url)
        return self
    
    def get_page_title(self) -> str:
        """Get contact page title."""
        return self.get_text(self.PAGE_TITLE)
    
    def is_contact_form_visible(self) -> bool:
        """Check if contact form is visible."""
        return self.is_element_visible(self.CONTACT_FORM)
    
    def fill_first_name(self, first_name: str):
        """Fill first name field."""
        return self.enter_text(self.FIRST_NAME_FIELD, first_name)
    
    def fill_last_name(self, last_name: str):
        """Fill last name field."""
        return self.enter_text(self.LAST_NAME_FIELD, last_name)
    
    def fill_email(self, email: str):
        """Fill email field."""
        return self.enter_text(self.EMAIL_FIELD, email)
    
    def fill_company(self, company: str):
        """Fill company field."""
        return self.enter_text(self.COMPANY_FIELD, company)
    
    def fill_phone(self, phone: str):
        """Fill phone field."""
        return self.enter_text(self.PHONE_FIELD, phone)
    
    def fill_subject(self, subject: str):
        """Fill subject field."""
        return self.enter_text(self.SUBJECT_FIELD, subject)
    
    def fill_message(self, message: str):
        """Fill message field."""
        return self.enter_text(self.MESSAGE_FIELD, message)
    
    def select_country(self, country: str):
        """Select country from dropdown."""
        if self.wait_for_element_visible(self.COUNTRY_DROPDOWN):
            from selenium.webdriver.support.ui import Select
            dropdown = self.find_element(self.COUNTRY_DROPDOWN)
            if dropdown:
                try:
                    select = Select(dropdown)
                    select.select_by_visible_text(country)
                    return True
                except Exception as e:
                    self.logger.error(f"Error selecting country: {str(e)}")
        return False
    
    def select_industry(self, industry: str):
        """Select industry from dropdown."""
        if self.wait_for_element_visible(self.INDUSTRY_DROPDOWN):
            from selenium.webdriver.support.ui import Select
            dropdown = self.find_element(self.INDUSTRY_DROPDOWN)
            if dropdown:
                try:
                    select = Select(dropdown)
                    select.select_by_visible_text(industry)
                    return True
                except Exception as e:
                    self.logger.error(f"Error selecting industry: {str(e)}")
        return False
    
    def select_company_size(self, size: str):
        """Select company size from dropdown."""
        if self.wait_for_element_visible(self.COMPANY_SIZE_DROPDOWN):
            from selenium.webdriver.support.ui import Select
            dropdown = self.find_element(self.COMPANY_SIZE_DROPDOWN)
            if dropdown:
                try:
                    select = Select(dropdown)
                    select.select_by_visible_text(size)
                    return True
                except Exception as e:
                    self.logger.error(f"Error selecting company size: {str(e)}")
        return False
    
    def submit_form(self):
        """Submit contact form."""
        return self.click_element(self.SUBMIT_BUTTON)
    
    def reset_form(self):
        """Reset contact form."""
        return self.click_element(self.RESET_BUTTON)
    
    def fill_contact_form(self, contact_data: Dict[str, str]):
        """Fill complete contact form."""
        success = True
        
        if 'first_name' in contact_data:
            success &= self.fill_first_name(contact_data['first_name'])
        
        if 'last_name' in contact_data:
            success &= self.fill_last_name(contact_data['last_name'])
        
        if 'email' in contact_data:
            success &= self.fill_email(contact_data['email'])
        
        if 'company' in contact_data:
            success &= self.fill_company(contact_data['company'])
        
        if 'phone' in contact_data:
            success &= self.fill_phone(contact_data['phone'])
        
        if 'subject' in contact_data:
            success &= self.fill_subject(contact_data['subject'])
        
        if 'message' in contact_data:
            success &= self.fill_message(contact_data['message'])
        
        if 'country' in contact_data:
            success &= self.select_country(contact_data['country'])
        
        if 'industry' in contact_data:
            success &= self.select_industry(contact_data['industry'])
        
        if 'company_size' in contact_data:
            success &= self.select_company_size(contact_data['company_size'])
        
        return success
    
    def get_success_message(self) -> str:
        """Get success message."""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self) -> str:
        """Get error message."""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed."""
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def get_contact_information(self) -> Dict[str, str]:
        """Get contact information from page."""
        contact_info = {}
        
        if self.is_element_present(self.EMAIL_ADDRESS):
            contact_info['email'] = self.get_text(self.EMAIL_ADDRESS)
        
        if self.is_element_present(self.PHONE_NUMBER):
            contact_info['phone'] = self.get_text(self.PHONE_NUMBER)
        
        if self.is_element_present(self.ADDRESS):
            contact_info['address'] = self.get_text(self.ADDRESS)
        
        return contact_info
    
    def get_social_media_links(self) -> List[str]:
        """Get social media links."""
        links = []
        social_elements = self.find_elements(self.SOCIAL_LINKS)
        
        for element in social_elements:
            href = element.get_attribute("href")
            if href:
                links.append(href)
        
        return links
    
    def is_map_section_visible(self) -> bool:
        """Check if map section is visible."""
        return self.is_element_visible(self.MAP_SECTION)
    
    def get_form_field_labels(self) -> List[str]:
        """Get all form field labels."""
        labels = []
        label_elements = self.find_elements((By.CSS_SELECTOR, "label"))
        
        for element in label_elements:
            text = element.text.strip()
            if text:
                labels.append(text)
        
        return labels
    
    def validate_required_fields(self) -> Dict[str, bool]:
        """Validate required fields."""
        validation = {}
        
        # Check if fields are marked as required
        required_fields = {
            'first_name': self.FIRST_NAME_FIELD,
            'last_name': self.LAST_NAME_FIELD,
            'email': self.EMAIL_FIELD,
            'company': self.COMPANY_FIELD,
            'message': self.MESSAGE_FIELD
        }
        
        for field_name, locator in required_fields.items():
            element = self.find_element(locator)
            if element:
                is_required = element.get_attribute("required") is not None
                validation[field_name] = is_required
        
        return validation
    
    def verify_contact_page_load(self) -> bool:
        """Verify contact page has loaded correctly."""
        return (
            bool(self.get_page_title()) and
            self.is_contact_form_visible()
        )