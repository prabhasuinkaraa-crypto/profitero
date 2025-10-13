@scrape
Feature: Scrape key SEO elements for auditing
  Collect page titles, H1-H3, and canonical links for a set of URLs.

  Scenario: Scrape SEO elements from pages
    Given I plan to scrape these paths
      | path            |
      | /               |
      | /about          |
      | /solutions      |
    When I scrape the pages
    Then I export the results to "artifacts/seo_audit.csv"
