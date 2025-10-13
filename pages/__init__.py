"""Page objects package for test framework."""
from .base_page import BasePage
from .home_page import HomePage
from .product_page import ProductPage
from .contact_page import ContactPage

__all__ = ['BasePage', 'HomePage', 'ProductPage', 'ContactPage']