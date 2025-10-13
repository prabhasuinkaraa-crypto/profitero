@api
Feature: Public site health and metadata
  Validate public endpoints for Profitero site

  Scenario: robots.txt is accessible and not empty
    When I GET "/robots.txt"
    Then the response status should be 200
    And the response body should not be empty

  Scenario: sitemap index or page sitemap is accessible
    When I GET "/sitemap.xml"
    Then the response status should be 200
    And the response body should contain "sitemap"
