"""Test helper utilities."""
import os
import time
import json
from datetime import datetime
from typing import Any, Dict, List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utils.config_reader import config
import logging


class TestHelpers:
    """Collection of test helper utilities."""
    
    def __init__(self, driver=None):
        """Initialize test helpers."""
        self.driver = driver
        self.logger = logging.getLogger(__name__)
    
    def take_screenshot(self, name: str = None) -> str:
        """Take screenshot and save to reports directory."""
        if not self.driver:
            return ""
        
        try:
            if not name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = f"screenshot_{timestamp}"
            
            screenshots_dir = config.get_screenshots_path()
            os.makedirs(screenshots_dir, exist_ok=True)
            
            filepath = os.path.join(screenshots_dir, f"{name}.png")
            self.driver.save_screenshot(filepath)
            
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return ""
    
    def wait_for_element(self, locator: tuple, timeout: int = None) -> bool:
        """Wait for element to be present."""
        if not self.driver:
            return False
        
        timeout = timeout or config.get_timeout()
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.warning(f"Element not found within {timeout} seconds: {locator}")
            return False
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> bool:
        """Wait for element to be clickable."""
        if not self.driver:
            return False
        
        timeout = timeout or config.get_timeout()
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            self.logger.warning(f"Element not clickable within {timeout} seconds: {locator}")
            return False
    
    def scroll_to_element(self, element):
        """Scroll to element."""
        if not self.driver or not element:
            return
        
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Small delay for smooth scrolling
        except Exception as e:
            self.logger.error(f"Error scrolling to element: {str(e)}")
    
    def get_page_performance_metrics(self) -> Dict[str, Any]:
        """Get page performance metrics."""
        if not self.driver:
            return {}
        
        try:
            # Get navigation timing
            nav_timing = self.driver.execute_script("""
                return {
                    loadEventEnd: performance.timing.loadEventEnd,
                    navigationStart: performance.timing.navigationStart,
                    domContentLoadedEventEnd: performance.timing.domContentLoadedEventEnd,
                    loadEventStart: performance.timing.loadEventStart
                };
            """)
            
            # Calculate metrics
            page_load_time = nav_timing['loadEventEnd'] - nav_timing['navigationStart']
            dom_ready_time = nav_timing['domContentLoadedEventEnd'] - nav_timing['navigationStart']
            
            return {
                'page_load_time_ms': page_load_time,
                'dom_ready_time_ms': dom_ready_time,
                'navigation_timing': nav_timing
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance metrics: {str(e)}")
            return {}
    
    def check_console_errors(self) -> List[Dict[str, Any]]:
        """Check for JavaScript console errors."""
        if not self.driver:
            return []
        
        try:
            logs = self.driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            return errors
        except Exception as e:
            self.logger.error(f"Error checking console errors: {str(e)}")
            return []
    
    def verify_links(self, links: List[str]) -> Dict[str, Any]:
        """Verify if links are accessible."""
        import requests
        
        results = {
            'working_links': [],
            'broken_links': [],
            'redirect_links': []
        }
        
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; TestBot/1.0)'})
        
        for link in links:
            try:
                response = session.head(link, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    results['working_links'].append(link)
                elif 300 <= response.status_code < 400:
                    results['redirect_links'].append({
                        'url': link,
                        'status_code': response.status_code,
                        'redirect_url': response.url
                    })
                else:
                    results['broken_links'].append({
                        'url': link,
                        'status_code': response.status_code
                    })
                    
            except Exception as e:
                results['broken_links'].append({
                    'url': link,
                    'error': str(e)
                })
        
        session.close()
        return results
    
    def generate_test_report(self, test_results: Dict[str, Any]) -> str:
        """Generate HTML test report."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Profitero Test Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .section {{ margin: 20px 0; }}
                    .pass {{ color: green; }}
                    .fail {{ color: red; }}
                    .warning {{ color: orange; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Profitero Website Test Report</h1>
                    <p>Generated on: {timestamp}</p>
                </div>
                
                <div class="section">
                    <h2>Test Summary</h2>
                    <p>Total Tests: {test_results.get('total_tests', 0)}</p>
                    <p class="pass">Passed: {test_results.get('passed', 0)}</p>
                    <p class="fail">Failed: {test_results.get('failed', 0)}</p>
                    <p class="warning">Skipped: {test_results.get('skipped', 0)}</p>
                </div>
                
                <div class="section">
                    <h2>Test Details</h2>
                    <pre>{json.dumps(test_results, indent=2)}</pre>
                </div>
            </body>
            </html>
            """
            
            reports_dir = config.get_reports_path()
            os.makedirs(reports_dir, exist_ok=True)
            
            report_file = os.path.join(reports_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Test report generated: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"Error generating test report: {str(e)}")
            return ""
    
    def wait_and_retry(self, func, max_retries: int = 3, delay: float = 1.0):
        """Retry function with delay."""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
    
    def validate_email_format(self, email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_url_format(self, url: str) -> bool:
        """Validate URL format."""
        import re
        pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        return re.match(pattern, url) is not None