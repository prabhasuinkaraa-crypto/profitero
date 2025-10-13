# Profitero Website Test Automation Framework

A comprehensive test automation framework for Profitero.com website testing, web scraping, and API automation using Python, Selenium, and BDD (Behavior-Driven Development) approach.

## 🚀 Features

### Web Testing
- **Page Object Model (POM)** - Maintainable and scalable page objects
- **Cross-browser Testing** - Chrome, Firefox, Edge support
- **Responsive Testing** - Mobile, tablet, desktop viewports
- **Accessibility Testing** - WCAG compliance checks
- **Performance Testing** - Page load times, Core Web Vitals

### BDD Framework
- **Gherkin Scenarios** - Human-readable test scenarios
- **Comprehensive Coverage** - Homepage, products, contact forms, security
- **Step Definitions** - Reusable step implementations
- **Test Data Management** - JSON-based test data with Faker integration

### Web Scraping
- **Intelligent Scraping** - Rate-limited, respectful scraping
- **Data Extraction** - Products, services, contact information
- **Content Monitoring** - Change detection and validation
- **Multiple Formats** - JSON, CSV export capabilities

### API Testing
- **REST API Automation** - Full CRUD operations testing
- **Authentication Testing** - Login, logout, token validation
- **Performance Testing** - Load, stress, concurrent user testing
- **Security Testing** - SQL injection, XSS, security headers

### Reporting
- **Multiple Formats** - HTML, JSON, CSV, JUnit XML
- **Rich HTML Reports** - Screenshots, performance metrics
- **Dashboard Data** - Test trends and analytics
- **Allure Integration** - Professional test reporting

## 📁 Project Structure

```
profitero-test-framework/
├── api_tests/                  # API test modules
│   ├── base_api_test.py       # Base API test class
│   ├── test_authentication_api.py
│   ├── test_products_api.py
│   └── test_performance_api.py
├── features/                   # BDD feature files
│   ├── steps/                 # Step definitions
│   ├── homepage.feature
│   ├── product_pages.feature
│   ├── contact_functionality.feature
│   ├── web_scraping.feature
│   ├── api_testing.feature
│   ├── cross_browser_testing.feature
│   ├── security_testing.feature
│   ├── performance_testing.feature
│   └── environment.py
├── pages/                      # Page Object Model
│   ├── base_page.py
│   ├── home_page.py
│   ├── product_page.py
│   └── contact_page.py
├── utils/                      # Utility modules
│   ├── config_reader.py
│   ├── driver_manager.py
│   ├── web_scraper.py
│   ├── test_helpers.py
│   ├── data_manager.py
│   └── report_generator.py
├── test_data/                  # Test data files
│   ├── test_users.json
│   ├── test_products.json
│   ├── contact_form_data.json
│   └── api_test_data.json
├── reports/                    # Generated reports
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Chrome/Firefox/Edge browser
- Git

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd profitero-test-framework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings**
   ```bash
   # Edit config.yaml to match your environment
   cp config.yaml config.local.yaml
   ```

## 🎯 Usage

### Running BDD Tests

**All tests:**
```bash
behave
```

**Specific feature:**
```bash
behave features/homepage.feature
```

**With tags:**
```bash
behave --tags=@smoke
behave --tags=@homepage,@products
```

**Generate Allure report:**
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
allure serve reports/allure-results
```

### Running API Tests

**All API tests:**
```bash
python -m pytest api_tests/ -v
```

**Specific test module:**
```bash
python -m pytest api_tests/test_products_api.py -v
```

**Performance tests:**
```bash
python -m pytest api_tests/test_performance_api.py -v
```

### Web Scraping

**Interactive scraping:**
```python
from utils.web_scraper import WebScraper

scraper = WebScraper()
homepage_data = scraper.scrape_homepage_data()
products_data = scraper.scrape_product_pages()
scraper.save_scraped_data(homepage_data, 'homepage_data.json')
```

**Command line scraping:**
```bash
python -c "
from utils.web_scraper import WebScraper
scraper = WebScraper()
data = scraper.scrape_homepage_data()
scraper.save_scraped_data(data, 'scraped_data.json')
"
```

### Cross-Browser Testing

**Chrome:**
```bash
behave -D browser=chrome
```

**Firefox:**
```bash
behave -D browser=firefox
```

**Headless mode:**
```bash
behave -D headless=true
```

## 📊 Test Categories

### Functional Testing
- ✅ Homepage functionality
- ✅ Product page navigation
- ✅ Contact form submission
- ✅ Search functionality
- ✅ User interactions

### Non-Functional Testing
- ⚡ Performance testing
- 🔒 Security testing
- 📱 Responsive design
- ♿ Accessibility compliance
- 🌐 Cross-browser compatibility

### API Testing
- 🔐 Authentication & authorization
- 📝 CRUD operations
- 📊 Data validation
- 🚀 Performance & load testing
- 🛡️ Security testing

### Web Scraping
- 📄 Content extraction
- 🔄 Change monitoring
- 📈 Data analysis
- 🤖 Automated collection

## 🔧 Configuration

### config.yaml
```yaml
# Base configuration
base_url: "https://www.profitero.com"
browser: "chrome"
headless: false
timeout: 30

# Test data paths
test_data_path: "test_data/"
reports_path: "reports/"
screenshots_path: "reports/screenshots/"

# Scraping settings
scraping:
  delay_between_requests: 2
  max_pages_to_scrape: 10
  user_agents:
    - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

## 📈 Reporting

### HTML Reports
Rich HTML reports with:
- Test execution summary
- Pass/fail statistics
- Screenshots on failures
- Performance metrics
- Environment information

### JSON Reports
Machine-readable reports for:
- CI/CD integration
- Data analysis
- Custom dashboards
- Trend analysis

### JUnit XML
Compatible with:
- Jenkins
- Azure DevOps
- GitHub Actions
- Other CI/CD tools

## 🧪 Test Data Management

### Static Test Data
- `test_users.json` - User credentials and profiles
- `test_products.json` - Product information
- `contact_form_data.json` - Form submission data
- `api_test_data.json` - API testing payloads

### Dynamic Test Data
```python
from utils.data_manager import DataManager

dm = DataManager()
fake_user = dm.generate_fake_user()
test_dataset = dm.create_test_dataset('users', 100)
```

## 🔒 Security Testing

### Implemented Tests
- SQL Injection detection
- XSS vulnerability testing
- CSRF protection validation
- Security headers verification
- Authentication bypass attempts

### Security Payloads
```python
security_payloads = {
    'sql_injection': ["'; DROP TABLE users; --", "1' OR '1'='1"],
    'xss': ["<script>alert('xss')</script>", "javascript:alert('xss')"],
    'path_traversal': ["../../../etc/passwd", "..\\..\\windows\\system32"]
}
```

## 🚀 Performance Testing

### Metrics Tracked
- Page load times
- Time to first byte (TTFB)
- Core Web Vitals (LCP, FID, CLS)
- API response times
- Concurrent user handling

### Load Testing
```python
# API load testing
results = test_concurrent_requests('/products', concurrent_count=50)
success_rate = results['successful_requests'] / results['total_requests']
```

## 🌐 Cross-Browser Support

### Supported Browsers
- **Chrome** - Latest stable version
- **Firefox** - Latest stable version  
- **Edge** - Latest stable version
- **Safari** - macOS only (with additional setup)

### Mobile Testing
- Responsive design validation
- Touch interaction testing
- Mobile-specific functionality

## 📱 Accessibility Testing

### WCAG Compliance
- Keyboard navigation
- Screen reader compatibility
- Color contrast validation
- Alt text verification
- Form label association

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Profitero Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: behave --tags=@smoke
      - name: Generate report
        run: allure generate reports/allure-results
```

## 🐛 Troubleshooting

### Common Issues

**WebDriver not found:**
```bash
# Install webdriver-manager
pip install webdriver-manager
```

**Permission denied on screenshots:**
```bash
chmod 755 reports/screenshots/
```

**Import errors:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Debug Mode
```bash
# Enable debug logging
behave --logging-level=DEBUG

# Run single scenario
behave features/homepage.feature:10
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for utilities
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Selenium WebDriver team
- Behave BDD framework
- Profitero team for the amazing platform
- Open source community

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the documentation
- Review existing test examples

---

**Happy Testing! 🧪✨**