#!/usr/bin/env python3
"""
Quick Start Example for Profitero Test Framework
Demonstrates basic usage of the framework components.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_manager import DriverManager
from utils.web_scraper import WebScraper
from utils.data_manager import DataManager
from utils.report_generator import ReportGenerator
from pages.home_page import HomePage
from api_tests.base_api_test import BaseAPITest


def demo_web_testing():
    """Demonstrate web testing capabilities."""
    print("🌐 Web Testing Demo")
    print("-" * 40)
    
    # Initialize driver
    driver_manager = DriverManager()
    driver = driver_manager.create_driver()
    
    try:
        # Test homepage
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        print(f"✅ Page Title: {home_page.get_page_title()}")
        print(f"✅ Logo Displayed: {home_page.is_logo_displayed()}")
        print(f"✅ Navigation Visible: {home_page.is_main_navigation_visible()}")
        
        # Get navigation links
        nav_links = home_page.get_all_navigation_links()
        print(f"✅ Found {len(nav_links)} navigation links")
        
        # Take screenshot
        screenshot_path = home_page.take_screenshot("demo_homepage")
        print(f"📸 Screenshot saved: {screenshot_path}")
        
    finally:
        driver_manager.quit_driver()
    
    print("✅ Web testing demo completed!\n")


def demo_web_scraping():
    """Demonstrate web scraping capabilities."""
    print("🕷️  Web Scraping Demo")
    print("-" * 40)
    
    # Initialize scraper
    scraper = WebScraper()
    
    try:
        # Scrape homepage data
        print("Scraping homepage data...")
        homepage_data = scraper.scrape_homepage_data()
        
        print(f"✅ Page Title: {homepage_data.get('title', 'N/A')}")
        print(f"✅ Products Found: {len(homepage_data.get('products', []))}")
        print(f"✅ Services Found: {len(homepage_data.get('services', []))}")
        print(f"✅ Footer Links: {len(homepage_data.get('footer_links', []))}")
        
        # Save scraped data
        scraper.save_scraped_data(homepage_data, 'demo_scraped_data.json')
        print("💾 Scraped data saved to demo_scraped_data.json")
        
    finally:
        scraper.close_session()
    
    print("✅ Web scraping demo completed!\n")


def demo_api_testing():
    """Demonstrate API testing capabilities."""
    print("🔌 API Testing Demo")
    print("-" * 40)
    
    # Initialize API test
    api_test = BaseAPITest()
    
    try:
        # Test health endpoint
        print("Testing API health endpoint...")
        response = api_test.get('/health')
        
        if response:
            print(f"✅ Health Check Status: {response.status_code}")
            print(f"✅ Response Time: {response.elapsed.total_seconds():.3f}s")
        else:
            print("❌ Health check endpoint not available")
        
        # Test products endpoint
        print("Testing products endpoint...")
        response = api_test.get('/products')
        
        if response:
            print(f"✅ Products API Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Response contains data: {bool(data)}")
                except:
                    print("✅ Response received (not JSON)")
        else:
            print("❌ Products endpoint not available")
        
        # Test rate limiting
        print("Testing rate limiting...")
        rate_results = api_test.test_rate_limiting('/products', requests_count=5)
        print(f"✅ Rate Limiting Test: {rate_results['successful_requests']}/{rate_results['total_requests']} successful")
        
    finally:
        api_test.cleanup()
    
    print("✅ API testing demo completed!\n")


def demo_data_management():
    """Demonstrate data management capabilities."""
    print("📊 Data Management Demo")
    print("-" * 40)
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Generate fake data
    print("Generating fake test data...")
    fake_user = data_manager.generate_fake_user()
    fake_contact = data_manager.generate_fake_contact_data()
    fake_product = data_manager.generate_fake_product()
    
    print(f"✅ Generated User: {fake_user['first_name']} {fake_user['last_name']}")
    print(f"✅ Generated Contact: {fake_contact['company']}")
    print(f"✅ Generated Product: {fake_product['name']}")
    
    # Load existing test data
    print("Loading test data...")
    users = data_manager.get_test_users('valid')
    products = data_manager.get_product_data('sample')
    
    print(f"✅ Loaded {len(users)} test users")
    print(f"✅ Loaded {len(products)} test products")
    
    # Get security test data
    security_data = data_manager.get_security_test_data()
    print(f"✅ Security payloads available: {list(security_data.keys())}")
    
    print("✅ Data management demo completed!\n")


def demo_reporting():
    """Demonstrate reporting capabilities."""
    print("📈 Reporting Demo")
    print("-" * 40)
    
    # Initialize report generator
    report_generator = ReportGenerator()
    
    # Sample test results
    test_results = {
        'total_tests': 25,
        'passed': 22,
        'failed': 2,
        'skipped': 1,
        'test_duration': 180,
        'scenarios': [
            {
                'name': 'Homepage loads successfully',
                'status': 'passed',
                'duration': 2.5,
                'tags': ['smoke', 'homepage']
            },
            {
                'name': 'Product page navigation',
                'status': 'passed',
                'duration': 3.2,
                'tags': ['products', 'navigation']
            },
            {
                'name': 'Contact form validation',
                'status': 'failed',
                'duration': 5.1,
                'tags': ['contact', 'forms'],
                'error_message': 'Email validation failed'
            }
        ]
    }
    
    # Generate reports
    print("Generating test reports...")
    
    html_report = report_generator.generate_html_report(test_results)
    json_report = report_generator.generate_json_report(test_results)
    csv_report = report_generator.generate_csv_report(test_results)
    
    print(f"✅ HTML Report: {html_report}")
    print(f"✅ JSON Report: {json_report}")
    print(f"✅ CSV Report: {csv_report}")
    
    # Generate dashboard data
    dashboard_data = report_generator.create_dashboard_data(test_results)
    print(f"✅ Dashboard data generated with {len(dashboard_data)} sections")
    
    print("✅ Reporting demo completed!\n")


def main():
    """Run all demos."""
    print("🚀 Profitero Test Framework - Quick Start Demo")
    print("=" * 60)
    print()
    
    try:
        # Run demos
        demo_web_testing()
        demo_web_scraping()
        demo_api_testing()
        demo_data_management()
        demo_reporting()
        
        print("🎉 All demos completed successfully!")
        print("\n📚 Next Steps:")
        print("1. Explore the features/ directory for BDD scenarios")
        print("2. Check api_tests/ for API testing examples")
        print("3. Review test_data/ for sample test data")
        print("4. Run: python run_tests.py --help for more options")
        print("5. Execute: behave --tags=@smoke for smoke tests")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        print("Please check your environment setup and dependencies.")
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)