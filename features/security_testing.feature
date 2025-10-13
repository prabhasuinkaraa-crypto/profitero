Feature: Security Testing
  As a QA engineer
  I want to test the security aspects of the Profitero website
  So that I can ensure user data and system integrity are protected

  @security @https
  Scenario: HTTPS enforcement
    Given I am testing the website security
    When I try to access the website via HTTP
    Then I should be redirected to HTTPS
    And the connection should be secure
    And the SSL certificate should be valid

  @security @headers
  Scenario: Security headers are present
    Given I am on the Profitero website
    When I inspect the HTTP response headers
    Then I should see security headers like:
      | header                        |
      | Strict-Transport-Security     |
      | X-Content-Type-Options        |
      | X-Frame-Options               |
      | Content-Security-Policy       |
      | X-XSS-Protection             |

  @security @forms
  Scenario: Form security measures
    Given I am on a page with forms
    When I inspect the form security
    Then forms should use HTTPS for submission
    And forms should have CSRF protection
    And sensitive data should not be exposed in URLs
    And form inputs should be properly sanitized

  @security @xss
  Scenario: Cross-Site Scripting (XSS) protection
    Given I am testing for XSS vulnerabilities
    When I try to inject malicious scripts
    Then the scripts should be blocked or sanitized
    And no malicious code should execute
    And user input should be properly escaped

  @security @clickjacking
  Scenario: Clickjacking protection
    Given I am testing for clickjacking vulnerabilities
    When I try to embed the website in an iframe
    Then the website should prevent iframe embedding
    And X-Frame-Options header should be set appropriately

  @security @sensitive_data
  Scenario: Sensitive data protection
    Given I am inspecting the website
    When I check for exposed sensitive information
    Then no API keys should be visible in client-side code
    And no passwords should be stored in plain text
    And no sensitive configuration should be exposed

  @security @session
  Scenario: Session security
    Given I am logged into the website
    When I test session management
    Then sessions should expire after appropriate time
    And session tokens should be secure
    And logout should properly invalidate sessions

  @security @input_validation
  Scenario: Input validation and sanitization
    Given I am testing form inputs
    When I enter various types of malicious input
    Then the system should validate and sanitize inputs
    And SQL injection attempts should be blocked
    And file upload restrictions should be enforced

  @security @cookies
  Scenario: Cookie security
    Given I am on the website
    When I inspect cookies
    Then sensitive cookies should be marked as HttpOnly
    And cookies should be marked as Secure over HTTPS
    And cookie expiration should be appropriate

  @security @error_handling
  Scenario: Secure error handling
    Given I am testing error scenarios
    When I trigger various errors
    Then error messages should not expose sensitive information
    And stack traces should not be visible to users
    And error pages should be user-friendly

  @security @file_upload
  Scenario: File upload security
    Given there are file upload features
    When I test file upload functionality
    Then only allowed file types should be accepted
    And file size limits should be enforced
    And uploaded files should be scanned for malware
    And file paths should be properly sanitized

  @security @rate_limiting
  Scenario: Rate limiting protection
    Given I am testing for rate limiting
    When I send multiple requests rapidly
    Then the system should implement rate limiting
    And excessive requests should be blocked
    And appropriate error messages should be returned

  @security @privacy
  Scenario: Privacy protection
    Given I am reviewing privacy measures
    When I check data collection practices
    Then personal data collection should be minimal
    And privacy policy should be accessible
    And user consent should be properly managed
    And data retention policies should be followed