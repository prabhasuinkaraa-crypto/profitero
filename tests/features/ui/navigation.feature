@ui
Feature: Profitero website core navigation
  As a visitor I can navigate to key pages and see expected content

  Background:
    Given I launch the browser

  Scenario Outline: Navigate to key top-level pages and verify hero text
    When I open path "<path>"
    Then I should see text containing "<expect>"

    Examples:
      | path                | expect                |
      | /                   | Profitero             |
      | /about              | About                 |
      | /solutions          | Solutions             |
      | /resources          | Resources             |
      | /request-a-demo     | Demo                  |

  Scenario: Navigation menu is present and clickable
    When I open path "/"
    Then the element "nav" should exist
    And the mobile menu toggle should be present if applicable
