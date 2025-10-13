Feature: Web Scraping Functionality
  As a QA engineer
  I want to scrape data from the Profitero website
  So that I can analyze content and perform data validation

  @scraping @homepage
  Scenario: Scrape homepage data successfully
    Given I have access to the Profitero website
    When I scrape the homepage data
    Then I should extract the page title
    And I should extract the meta description
    And I should extract all navigation links
    And I should extract product information
    And I should extract service information
    And I should extract footer links

  @scraping @products
  Scenario: Scrape all product pages
    Given I have access to the Profitero website
    When I scrape all product pages
    Then I should extract product titles
    And I should extract product descriptions
    And I should extract product features
    And I should extract product benefits
    And I should extract product images
    And I should save the scraped data to JSON files

  @scraping @content_validation
  Scenario: Validate scraped content quality
    Given I have scraped website data
    When I analyze the scraped content
    Then all product pages should have titles
    And all product pages should have descriptions
    And all images should have valid URLs
    And all links should be properly formatted
    And there should be no duplicate content

  @scraping @performance
  Scenario: Scraping performance and rate limiting
    Given I am scraping the website
    When I implement rate limiting between requests
    Then I should wait between requests to avoid overloading the server
    And I should handle HTTP errors gracefully
    And I should retry failed requests with exponential backoff
    And the scraping should complete within reasonable time

  @scraping @data_extraction
  Scenario: Extract specific data points
    Given I am scraping product pages
    When I extract structured data
    Then I should identify pricing information if available
    And I should extract contact information
    And I should extract company information
    And I should extract testimonials and reviews
    And I should extract technical specifications

  @scraping @selenium
  Scenario: Scrape dynamic content with Selenium
    Given I am using Selenium for scraping
    When I navigate to pages with dynamic content
    Then I should wait for JavaScript to load
    And I should extract content loaded by AJAX
    And I should handle pop-ups and modals
    And I should capture screenshots of pages

  @scraping @error_handling
  Scenario: Handle scraping errors gracefully
    Given I am scraping the website
    When I encounter HTTP errors
    Then I should log the errors appropriately
    And I should continue scraping other pages
    And I should retry failed requests
    And I should provide a summary of failed scrapes

  @scraping @data_storage
  Scenario: Store scraped data efficiently
    Given I have scraped website data
    When I save the data
    Then I should save data in JSON format
    And I should organize data by page type
    And I should include metadata like scrape timestamp
    And I should validate data integrity before saving

  @scraping @robots_compliance
  Scenario: Respect robots.txt and scraping ethics
    Given I am setting up web scraping
    When I check the robots.txt file
    Then I should respect the crawl delay
    And I should avoid scraping disallowed paths
    And I should use appropriate user agent strings
    And I should implement polite scraping practices

  @scraping @content_monitoring
  Scenario: Monitor content changes
    Given I have baseline scraped data
    When I scrape the website again
    Then I should compare with previous data
    And I should identify content changes
    And I should report new products or services
    And I should detect broken links or missing content