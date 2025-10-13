"""Behave environment configuration for test execution."""
import os
import logging
from behave import fixture, use_fixture
from utils.driver_manager import DriverManager
from utils.config_reader import config
from utils.web_scraper import WebScraper
from utils.test_helpers import TestHelpers


def before_all(context):
    """Set up test environment before all tests."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('test_execution.log'),
            logging.StreamHandler()
        ]
    )
    
    context.logger = logging.getLogger(__name__)
    context.logger.info("Starting test execution")
    
    # Create reports directory
    os.makedirs(config.get_reports_path(), exist_ok=True)
    os.makedirs(config.get_screenshots_path(), exist_ok=True)
    os.makedirs(config.get_test_data_path(), exist_ok=True)
    
    # Initialize test context
    context.config = config
    context.base_url = config.get_base_url()
    context.test_results = {
        'total_tests': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'scenarios': []
    }


def before_feature(context, feature):
    """Set up before each feature."""
    context.logger.info(f"Starting feature: {feature.name}")
    context.feature_name = feature.name


def before_scenario(context, scenario):
    """Set up before each scenario."""
    context.logger.info(f"Starting scenario: {scenario.name}")
    context.scenario_name = scenario.name
    context.test_results['total_tests'] += 1
    
    # Initialize driver for web tests
    if any(tag in scenario.tags for tag in ['homepage', 'products', 'contact', 'cross_browser', 'performance']):
        context.driver_manager = DriverManager()
        context.driver = context.driver_manager.create_driver()
        context.helpers = TestHelpers(context.driver)
        context.web_scraper = WebScraper(context.driver)
    
    # Initialize web scraper for scraping tests
    if 'scraping' in scenario.tags:
        context.web_scraper = WebScraper()
    
    # Set up API testing context
    if 'api' in scenario.tags:
        context.api_base_url = config.get_api_base_url()
        context.api_timeout = config.get('api_timeout', 30)
        context.api_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Profitero-Test-Suite/1.0'
        }


def after_scenario(context, scenario):
    """Clean up after each scenario."""
    scenario_result = {
        'name': scenario.name,
        'status': scenario.status.name,
        'tags': list(scenario.tags),
        'duration': getattr(scenario, 'duration', 0)
    }
    
    if scenario.status.name == 'passed':
        context.test_results['passed'] += 1
        context.logger.info(f"Scenario passed: {scenario.name}")
    elif scenario.status.name == 'failed':
        context.test_results['failed'] += 1
        context.logger.error(f"Scenario failed: {scenario.name}")
        
        # Take screenshot on failure if driver is available
        if hasattr(context, 'driver') and context.driver:
            screenshot_name = f"failed_{scenario.name.replace(' ', '_')}"
            context.helpers.take_screenshot(screenshot_name)
            scenario_result['screenshot'] = screenshot_name
    else:
        context.test_results['skipped'] += 1
        context.logger.warning(f"Scenario skipped: {scenario.name}")
    
    context.test_results['scenarios'].append(scenario_result)
    
    # Clean up driver
    if hasattr(context, 'driver_manager') and context.driver_manager:
        context.driver_manager.quit_driver()
    
    # Clean up web scraper
    if hasattr(context, 'web_scraper') and context.web_scraper:
        context.web_scraper.close_session()


def after_feature(context, feature):
    """Clean up after each feature."""
    context.logger.info(f"Completed feature: {feature.name}")


def after_all(context):
    """Clean up after all tests."""
    context.logger.info("Test execution completed")
    
    # Generate test report
    if hasattr(context, 'helpers'):
        report_file = context.helpers.generate_test_report(context.test_results)
        context.logger.info(f"Test report generated: {report_file}")
    
    # Log test summary
    results = context.test_results
    context.logger.info(f"Test Summary - Total: {results['total_tests']}, "
                       f"Passed: {results['passed']}, "
                       f"Failed: {results['failed']}, "
                       f"Skipped: {results['skipped']}")


@fixture
def browser_context(context, browser_name="chrome"):
    """Fixture for browser-specific testing."""
    original_browser = config.get_browser()
    
    # Temporarily change browser configuration
    config._config['browser'] = browser_name
    
    driver_manager = DriverManager()
    driver = driver_manager.create_driver()
    
    context.driver = driver
    context.driver_manager = driver_manager
    context.helpers = TestHelpers(driver)
    
    yield context
    
    # Clean up
    driver_manager.quit_driver()
    
    # Restore original browser configuration
    config._config['browser'] = original_browser


def use_browser(context, browser_name):
    """Use specific browser for testing."""
    use_fixture(browser_context, context, browser_name=browser_name)