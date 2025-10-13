@api
Feature: Basic content checks via HTTP
  Validate typical marketing pages return 200 and contain expected signals.

  Scenario Outline: Page returns 200 and contains expected word
    When I GET "<path>"
    Then the response status should be 200
    And the response body should contain "<word>"

    Examples:
      | path                 | word       |
      | /                    | Profitero  |
      | /about               | Profitero  |
      | /solutions/amazon    | Amazon     |
