#!/usr/bin/env python3
"""
Profitero Test Runner
Main script to execute different types of tests with various options.
"""

import argparse
import os
import sys
import subprocess
import logging
from datetime import datetime
from utils.config_reader import config
from utils.report_generator import ReportGenerator
from utils.data_manager import DataManager


def setup_logging():
    """Set up logging configuration."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f'test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def run_bdd_tests(args, logger):
    """Run BDD tests using Behave."""
    logger.info("Starting BDD tests execution")
    
    cmd = ['behave']
    
    # Add feature file if specified
    if args.feature:
        cmd.append(f'features/{args.feature}.feature')
    
    # Add tags if specified
    if args.tags:
        cmd.extend(['--tags', args.tags])
    
    # Add browser configuration
    if args.browser:
        cmd.extend(['-D', f'browser={args.browser}'])
    
    # Add headless mode
    if args.headless:
        cmd.extend(['-D', 'headless=true'])
    
    # Add output format
    if args.format:
        if args.format == 'allure':
            cmd.extend(['-f', 'allure_behave.formatter:AllureFormatter'])
            cmd.extend(['-o', 'reports/allure-results'])
        elif args.format == 'json':
            cmd.extend(['-f', 'json'])
            cmd.extend(['-o', 'reports/behave_results.json'])
    
    # Add parallel execution if specified
    if args.parallel:
        cmd.extend(['--processes', str(args.parallel)])
    
    # Execute command
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        logger.info(f"BDD tests completed with exit code: {result.returncode}")
        
        if result.stdout:
            logger.info("STDOUT:")
            logger.info(result.stdout)
        
        if result.stderr:
            logger.error("STDERR:")
            logger.error(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"Error running BDD tests: {e}")
        return False


def run_api_tests(args, logger):
    """Run API tests using pytest."""
    logger.info("Starting API tests execution")
    
    cmd = ['python', '-m', 'pytest', 'api_tests/', '-v']
    
    # Add specific test file if specified
    if args.test_file:
        cmd = ['python', '-m', 'pytest', f'api_tests/{args.test_file}', '-v']
    
    # Add markers/tags
    if args.markers:
        cmd.extend(['-m', args.markers])
    
    # Add output format
    if args.format:
        if args.format == 'junit':
            cmd.extend(['--junit-xml=reports/junit_results.xml'])
        elif args.format == 'html':
            cmd.extend(['--html=reports/pytest_report.html', '--self-contained-html'])
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(['-n', str(args.parallel)])
    
    # Execute command
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        logger.info(f"API tests completed with exit code: {result.returncode}")
        
        if result.stdout:
            logger.info("STDOUT:")
            logger.info(result.stdout)
        
        if result.stderr and result.returncode != 0:
            logger.error("STDERR:")
            logger.error(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"Error running API tests: {e}")
        return False


def run_web_scraping(args, logger):
    """Run web scraping tasks."""
    logger.info("Starting web scraping")
    
    try:
        from utils.web_scraper import WebScraper
        
        scraper = WebScraper()
        
        if args.scrape_type == 'homepage' or args.scrape_type == 'all':
            logger.info("Scraping homepage data")
            homepage_data = scraper.scrape_homepage_data()
            scraper.save_scraped_data(homepage_data, 'homepage_scraped.json')
        
        if args.scrape_type == 'products' or args.scrape_type == 'all':
            logger.info("Scraping product pages")
            products_data = scraper.scrape_product_pages()
            scraper.save_scraped_data(products_data, 'products_scraped.json')
        
        if args.scrape_type == 'contact' or args.scrape_type == 'all':
            logger.info("Scraping contact information")
            contact_info = scraper.extract_contact_info()
            scraper.save_scraped_data(contact_info, 'contact_scraped.json')
        
        scraper.close_session()
        logger.info("Web scraping completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during web scraping: {e}")
        return False


def generate_reports(args, logger):
    """Generate test reports."""
    logger.info("Generating test reports")
    
    try:
        report_generator = ReportGenerator()
        
        # Mock test results for demonstration
        # In real scenario, this would come from actual test execution
        test_results = {
            'total_tests': 50,
            'passed': 45,
            'failed': 3,
            'skipped': 2,
            'test_duration': 300,
            'scenarios': [
                {
                    'name': 'Homepage loads successfully',
                    'status': 'passed',
                    'duration': 2.5,
                    'tags': ['smoke', 'homepage']
                },
                {
                    'name': 'Contact form submission',
                    'status': 'failed',
                    'duration': 5.2,
                    'tags': ['contact', 'forms'],
                    'error_message': 'Form validation failed'
                }
            ]
        }
        
        if args.report_format == 'all':
            reports = report_generator.generate_all_reports(test_results)
            for format_type, file_path in reports.items():
                if file_path:
                    logger.info(f"Generated {format_type} report: {file_path}")
        else:
            if args.report_format == 'html':
                report_path = report_generator.generate_html_report(test_results)
            elif args.report_format == 'json':
                report_path = report_generator.generate_json_report(test_results)
            elif args.report_format == 'csv':
                report_path = report_generator.generate_csv_report(test_results)
            elif args.report_format == 'junit':
                report_path = report_generator.generate_junit_xml_report(test_results)
            
            if report_path:
                logger.info(f"Generated report: {report_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        return False


def setup_test_environment(args, logger):
    """Set up test environment."""
    logger.info("Setting up test environment")
    
    try:
        # Create necessary directories
        directories = [
            config.get_reports_path(),
            config.get_screenshots_path(),
            config.get_test_data_path()
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        
        # Initialize data manager
        data_manager = DataManager()
        
        # Generate test data if requested
        if args.generate_test_data:
            logger.info("Generating test data")
            data_manager.create_test_dataset('users', 10, 'generated_users.json')
            data_manager.create_test_dataset('products', 5, 'generated_products.json')
            data_manager.create_test_dataset('contacts', 15, 'generated_contacts.json')
        
        logger.info("Test environment setup completed")
        return True
        
    except Exception as e:
        logger.error(f"Error setting up test environment: {e}")
        return False


def cleanup_test_environment(args, logger):
    """Clean up test environment."""
    logger.info("Cleaning up test environment")
    
    try:
        # Clean up temporary files
        data_manager = DataManager()
        cleaned_files = data_manager.cleanup_test_data()
        logger.info(f"Cleaned up {cleaned_files} temporary files")
        
        # Clean up old reports
        report_generator = ReportGenerator()
        cleaned_reports = report_generator.cleanup_old_reports(days_to_keep=args.keep_reports)
        logger.info(f"Cleaned up {cleaned_reports} old reports")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        return False


def main():
    """Main function to parse arguments and execute tests."""
    parser = argparse.ArgumentParser(description='Profitero Test Automation Framework')
    
    # Test type selection
    parser.add_argument('--type', choices=['bdd', 'api', 'scraping', 'all'], 
                       default='bdd', help='Type of tests to run')
    
    # BDD specific options
    parser.add_argument('--feature', help='Specific feature file to run (without .feature extension)')
    parser.add_argument('--tags', help='Tags to filter scenarios (e.g., @smoke,@regression)')
    
    # API specific options
    parser.add_argument('--test-file', help='Specific API test file to run')
    parser.add_argument('--markers', help='Pytest markers to filter tests')
    
    # Web scraping options
    parser.add_argument('--scrape-type', choices=['homepage', 'products', 'contact', 'all'],
                       default='all', help='Type of content to scrape')
    
    # Browser options
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'edge'], 
                       default='chrome', help='Browser to use for tests')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    # Execution options
    parser.add_argument('--parallel', type=int, help='Number of parallel processes')
    parser.add_argument('--format', choices=['allure', 'json', 'html', 'junit'], 
                       help='Output format for test results')
    
    # Report options
    parser.add_argument('--generate-reports', action='store_true', help='Generate test reports')
    parser.add_argument('--report-format', choices=['html', 'json', 'csv', 'junit', 'all'],
                       default='html', help='Report format to generate')
    
    # Environment options
    parser.add_argument('--setup', action='store_true', help='Set up test environment')
    parser.add_argument('--cleanup', action='store_true', help='Clean up test environment')
    parser.add_argument('--generate-test-data', action='store_true', help='Generate test data')
    parser.add_argument('--keep-reports', type=int, default=30, help='Days to keep old reports')
    
    # Logging options
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet output')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    logger.info("=" * 60)
    logger.info("Profitero Test Automation Framework")
    logger.info("=" * 60)
    
    success = True
    
    try:
        # Set up environment if requested
        if args.setup:
            success &= setup_test_environment(args, logger)
        
        # Run tests based on type
        if args.type == 'bdd' or args.type == 'all':
            success &= run_bdd_tests(args, logger)
        
        if args.type == 'api' or args.type == 'all':
            success &= run_api_tests(args, logger)
        
        if args.type == 'scraping':
            success &= run_web_scraping(args, logger)
        
        # Generate reports if requested
        if args.generate_reports:
            success &= generate_reports(args, logger)
        
        # Clean up if requested
        if args.cleanup:
            success &= cleanup_test_environment(args, logger)
        
        # Final status
        if success:
            logger.info("✅ All operations completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Some operations failed. Check logs for details.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("⏹️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()