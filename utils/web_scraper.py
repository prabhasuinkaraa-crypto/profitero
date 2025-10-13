"""Web scraping utilities for Profitero website."""
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import Dict, List, Optional, Any
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config_reader import config
import logging


class WebScraper:
    """Web scraping utilities for Profitero website."""
    
    def __init__(self, driver=None):
        """Initialize web scraper."""
        self.driver = driver
        self.session = requests.Session()
        self.base_url = config.get_base_url()
        self.delay = config.get('scraping.delay_between_requests', 2)
        self.max_pages = config.get('scraping.max_pages_to_scrape', 10)
        self.user_agents = config.get('scraping.user_agents', [])
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Set random user agent
        if self.user_agents:
            self.session.headers.update({
                'User-Agent': random.choice(self.user_agents)
            })
    
    def scrape_homepage_data(self) -> Dict[str, Any]:
        """Scrape data from Profitero homepage."""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'title': soup.find('title').text if soup.find('title') else '',
                'meta_description': '',
                'navigation_links': [],
                'hero_section': {},
                'products': [],
                'services': [],
                'footer_links': []
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                data['meta_description'] = meta_desc.get('content', '')
            
            # Extract navigation links
            nav_links = soup.find_all('a', class_='navbar_dropdown-link')
            for link in nav_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if href and text:
                    data['navigation_links'].append({'text': text, 'href': href})
            
            # Extract product information
            product_links = soup.find_all('a', href=lambda x: x and '/product/' in x)
            for link in product_links:
                product_name = link.get_text(strip=True)
                product_url = link.get('href', '')
                if product_name and product_url:
                    data['products'].append({'name': product_name, 'url': product_url})
            
            # Extract service information
            service_links = soup.find_all('a', href=lambda x: x and '/services/' in x)
            for link in service_links:
                service_name = link.get_text(strip=True)
                service_url = link.get('href', '')
                if service_name and service_url:
                    data['services'].append({'name': service_name, 'url': service_url})
            
            # Extract footer links
            footer_links = soup.find_all('a', class_='footer-link-block')
            for link in footer_links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                if text and href:
                    data['footer_links'].append({'text': text, 'href': href})
            
            self.logger.info(f"Successfully scraped homepage data: {len(data['products'])} products, {len(data['services'])} services")
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping homepage: {str(e)}")
            return {}
    
    def scrape_product_pages(self) -> List[Dict[str, Any]]:
        """Scrape all product pages."""
        products_data = []
        
        # Get product URLs from homepage
        homepage_data = self.scrape_homepage_data()
        product_urls = [p['url'] for p in homepage_data.get('products', [])]
        
        for url in product_urls[:self.max_pages]:
            try:
                time.sleep(self.delay)  # Rate limiting
                
                full_url = url if url.startswith('http') else f"{self.base_url}{url}"
                response = self.session.get(full_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                product_data = {
                    'url': full_url,
                    'title': soup.find('title').text if soup.find('title') else '',
                    'heading': '',
                    'description': '',
                    'features': [],
                    'benefits': [],
                    'images': []
                }
                
                # Extract main heading
                h1 = soup.find('h1')
                if h1:
                    product_data['heading'] = h1.get_text(strip=True)
                
                # Extract description
                desc_elements = soup.find_all('p', class_=['description', 'product-description'])
                if desc_elements:
                    product_data['description'] = ' '.join([p.get_text(strip=True) for p in desc_elements])
                
                # Extract features
                feature_elements = soup.find_all('li')
                for feature in feature_elements:
                    text = feature.get_text(strip=True)
                    if text and len(text) > 10:  # Filter out short/empty text
                        product_data['features'].append(text)
                
                # Extract images
                img_elements = soup.find_all('img')
                for img in img_elements:
                    src = img.get('src', '')
                    alt = img.get('alt', '')
                    if src and 'cdn.prod.website-files.com' in src:
                        product_data['images'].append({'src': src, 'alt': alt})
                
                products_data.append(product_data)
                self.logger.info(f"Scraped product page: {product_data['title']}")
                
            except Exception as e:
                self.logger.error(f"Error scraping product page {url}: {str(e)}")
                continue
        
        return products_data
    
    def scrape_with_selenium(self, url: str) -> Dict[str, Any]:
        """Scrape dynamic content using Selenium."""
        if not self.driver:
            raise ValueError("Selenium driver not provided")
        
        try:
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            data = {
                'url': url,
                'title': self.driver.title,
                'current_url': self.driver.current_url,
                'page_source_length': len(self.driver.page_source),
                'cookies': self.driver.get_cookies(),
                'local_storage': {},
                'session_storage': {}
            }
            
            # Get local storage data
            try:
                local_storage_script = "return Object.keys(localStorage).reduce((obj, key) => { obj[key] = localStorage.getItem(key); return obj; }, {});"
                data['local_storage'] = self.driver.execute_script(local_storage_script)
            except Exception:
                pass
            
            # Get session storage data
            try:
                session_storage_script = "return Object.keys(sessionStorage).reduce((obj, key) => { obj[key] = sessionStorage.getItem(key); return obj; }, {});"
                data['session_storage'] = self.driver.execute_script(session_storage_script)
            except Exception:
                pass
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping with Selenium: {str(e)}")
            return {}
    
    def extract_contact_info(self) -> Dict[str, Any]:
        """Extract contact information from the website."""
        try:
            contact_url = f"{self.base_url}/contact"
            response = self.session.get(contact_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            contact_info = {
                'email_addresses': [],
                'phone_numbers': [],
                'addresses': [],
                'social_links': []
            }
            
            # Extract email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            import re
            emails = re.findall(email_pattern, soup.get_text())
            contact_info['email_addresses'] = list(set(emails))
            
            # Extract social media links
            social_links = soup.find_all('a', href=lambda x: x and any(social in x for social in ['linkedin', 'twitter', 'facebook', 'instagram', 'youtube']))
            for link in social_links:
                href = link.get('href', '')
                if href:
                    contact_info['social_links'].append(href)
            
            return contact_info
            
        except Exception as e:
            self.logger.error(f"Error extracting contact info: {str(e)}")
            return {}
    
    def save_scraped_data(self, data: Dict[str, Any], filename: str):
        """Save scraped data to JSON file."""
        try:
            filepath = f"{config.get_test_data_path()}{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved scraped data to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
    
    def close_session(self):
        """Close the requests session."""
        if self.session:
            self.session.close()