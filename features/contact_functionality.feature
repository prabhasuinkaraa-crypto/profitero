Feature: Contact Functionality
  As a potential customer
  I want to contact Profitero
  So that I can get more information about their services

  Background:
    Given I am on the Profitero contact page

  @smoke @contact
  Scenario: Contact page loads successfully
    Then I should see the contact page title
    And I should see the contact form
    And I should see contact information
    And the page URL should contain "contact"

  @contact @form
  Scenario: Contact form has all required fields
    Then I should see a "First Name" field
    And I should see a "Last Name" field
    And I should see an "Email" field
    And I should see a "Company" field
    And I should see a "Message" field
    And I should see a submit button

  @contact @form @positive
  Scenario: Submit contact form with valid data
    When I fill in the contact form with valid data:
      | field      | value                    |
      | first_name | John                     |
      | last_name  | Doe                      |
      | email      | john.doe@example.com     |
      | company    | Test Company             |
      | phone      | +1-555-123-4567          |
      | message    | I'm interested in your products |
    And I submit the contact form
    Then I should see a success message
    Or I should be redirected to a thank you page

  @contact @form @negative
  Scenario: Submit contact form with missing required fields
    When I submit the contact form without filling required fields
    Then I should see validation error messages
    And the form should not be submitted
    And I should remain on the contact page

  @contact @form @negative
  Scenario Outline: Submit contact form with invalid email
    When I fill in the email field with "<invalid_email>"
    And I submit the contact form
    Then I should see an email validation error
    And the form should not be submitted

    Examples:
      | invalid_email    |
      | invalid-email    |
      | @example.com     |
      | test@           |
      | test.example     |

  @contact @form @validation
  Scenario: Form field validation works correctly
    When I enter invalid data in form fields
    Then I should see real-time validation messages
    When I correct the invalid data
    Then the validation messages should disappear

  @contact @information
  Scenario: Contact information is displayed
    Then I should see the company email address
    And I should see the company phone number
    And I should see the company address
    And I should see social media links

  @contact @map
  Scenario: Office location map is displayed
    If there is a map section on the page
    Then the map should load successfully
    And the map should show the office location
    And the map should be interactive

  @contact @social
  Scenario: Social media links work correctly
    When I click on social media links
    Then they should open in new tabs
    And they should redirect to the correct social media profiles

  @contact @responsive
  Scenario: Contact page is responsive
    When I resize the browser to mobile view
    Then the contact form should be usable on mobile
    And contact information should be readable
    And the layout should adapt to mobile screen

  @contact @accessibility
  Scenario: Contact form is accessible
    Then all form fields should have proper labels
    And form fields should be keyboard accessible
    And error messages should be screen reader friendly
    And the form should have proper tab order

  @contact @performance
  Scenario: Contact page performance
    When I measure the contact page load time
    Then the page should load in less than 3 seconds
    And there should be no JavaScript console errors
    And the form should be interactive immediately

  @contact @security
  Scenario: Contact form security measures
    When I inspect the contact form
    Then the form should use HTTPS
    And the form should have CSRF protection
    And sensitive data should be handled securely

  @contact @multiple_submissions
  Scenario: Handle multiple form submissions
    When I submit the contact form successfully
    And I try to submit the same form again
    Then the system should handle duplicate submissions appropriately
    And I should receive appropriate feedback