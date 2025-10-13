Feature: API Testing
  As a QA engineer
  I want to test Profitero's API endpoints
  So that I can ensure backend services are working correctly

  @api @smoke
  Scenario: API health check
    Given I have access to the Profitero API
    When I send a GET request to the health check endpoint
    Then I should receive a 200 status code
    And the response should contain health status information

  @api @authentication
  Scenario: API authentication works correctly
    Given I have valid API credentials
    When I authenticate with the API
    Then I should receive a valid authentication token
    And the token should have appropriate expiration time
    And I should be able to use the token for subsequent requests

  @api @authentication @negative
  Scenario: API authentication fails with invalid credentials
    Given I have invalid API credentials
    When I try to authenticate with the API
    Then I should receive a 401 unauthorized status code
    And the response should contain an appropriate error message

  @api @data_retrieval
  Scenario: Retrieve product data via API
    Given I am authenticated with the API
    When I send a GET request to the products endpoint
    Then I should receive a 200 status code
    And the response should contain product information
    And the response should be in valid JSON format
    And each product should have required fields

  @api @data_validation
  Scenario: Validate API response data structure
    Given I am authenticated with the API
    When I retrieve data from various endpoints
    Then all responses should have consistent structure
    And all required fields should be present
    And data types should match the API specification
    And there should be no null values in required fields

  @api @rate_limiting
  Scenario: API rate limiting works correctly
    Given I am authenticated with the API
    When I send multiple requests rapidly
    Then I should encounter rate limiting after exceeding the limit
    And I should receive a 429 status code
    And the response should include rate limit headers

  @api @error_handling
  Scenario: API error handling
    Given I am authenticated with the API
    When I send requests with invalid parameters
    Then I should receive appropriate error status codes
    And error responses should contain helpful error messages
    And error responses should follow consistent format

  @api @pagination
  Scenario: API pagination works correctly
    Given I am authenticated with the API
    When I request paginated data
    Then I should receive pagination metadata
    And I should be able to navigate through pages
    And the total count should be accurate
    And page sizes should be respected

  @api @filtering
  Scenario: API filtering and search functionality
    Given I am authenticated with the API
    When I apply filters to API requests
    Then I should receive filtered results
    And the results should match the filter criteria
    And I should be able to combine multiple filters
    And invalid filters should return appropriate errors

  @api @performance
  Scenario: API performance testing
    Given I am authenticated with the API
    When I measure API response times
    Then responses should be returned within acceptable time limits
    And the API should handle concurrent requests efficiently
    And there should be no memory leaks or performance degradation

  @api @data_integrity
  Scenario: API data integrity checks
    Given I am authenticated with the API
    When I retrieve the same data multiple times
    Then the data should be consistent across requests
    And data relationships should be maintained
    And there should be no data corruption

  @api @security
  Scenario: API security testing
    Given I have access to the API
    When I test for common security vulnerabilities
    Then the API should be protected against SQL injection
    And the API should be protected against XSS attacks
    And sensitive data should not be exposed in responses
    And proper HTTPS should be enforced

  @api @versioning
  Scenario: API versioning support
    Given I am testing different API versions
    When I specify API version in requests
    Then I should receive responses appropriate to that version
    And deprecated versions should return appropriate warnings
    And version compatibility should be maintained

  @api @monitoring
  Scenario: API monitoring and logging
    Given I am making API requests
    When I check API logs and monitoring
    Then all requests should be properly logged
    And error rates should be within acceptable limits
    And response times should be monitored
    And alerts should be triggered for anomalies