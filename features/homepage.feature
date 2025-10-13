Feature: Profitero Homepage Functionality
  As a potential customer
  I want to navigate and interact with the Profitero homepage
  So that I can learn about their products and services

  Background:
    Given I am on the Profitero homepage

  @smoke @homepage
  Scenario: Homepage loads successfully
    Then I should see the Profitero logo
    And I should see the main navigation menu
    And I should see the hero section
    And the page title should contain "Profitero"

  @homepage @navigation
  Scenario: Main navigation menu is functional
    When I hover over the Products menu
    Then I should see the products dropdown menu
    And I should see "Digital Shelf" in the dropdown
    And I should see "Sales & Share" in the dropdown
    And I should see "Content Optimizer" in the dropdown
    And I should see "Shelf Intelligent Media" in the dropdown
    And I should see "Autopilot" in the dropdown

  @homepage @navigation
  Scenario: Top navigation links work correctly
    When I click on "About" in the top navigation
    Then I should be redirected to the About page
    When I go back to homepage
    And I click on "Careers" in the top navigation
    Then I should be redirected to the Careers page
    When I go back to homepage
    And I click on "Contact" in the top navigation
    Then I should be redirected to the Contact page

  @homepage @cta
  Scenario: Request demo button is functional
    When I click on "Request a demo" button
    Then I should be redirected to the demo request page
    Or I should see a demo request form

  @homepage @products
  Scenario Outline: Product navigation from homepage
    When I hover over the Products menu
    And I click on "<product_name>"
    Then I should be redirected to the "<product_name>" product page
    And the page should contain product information

    Examples:
      | product_name              |
      | Digital Shelf             |
      | Sales & Share             |
      | Content Optimizer         |
      | Shelf Intelligent Media   |
      | Autopilot                 |

  @homepage @footer
  Scenario: Footer contains all required links
    When I scroll to the footer
    Then I should see footer links for "Products"
    And I should see footer links for "Services"
    And I should see footer links for "Solutions"
    And I should see footer links for "Resources"
    And I should see social media links

  @homepage @responsive
  Scenario: Homepage is responsive
    When I resize the browser to mobile view
    Then the navigation menu should adapt to mobile layout
    And the hero section should be responsive
    When I resize the browser to tablet view
    Then the layout should adapt accordingly
    When I resize the browser to desktop view
    Then the layout should return to desktop format

  @homepage @performance
  Scenario: Homepage loads within acceptable time
    When I measure the page load time
    Then the page should load in less than 5 seconds
    And there should be no JavaScript console errors
    And all images should load successfully

  @homepage @seo
  Scenario: Homepage has proper SEO elements
    Then the page should have a proper title tag
    And the page should have a meta description
    And the page should have proper heading structure
    And the page should have alt text for images

  @homepage @accessibility
  Scenario: Homepage meets accessibility standards
    Then all interactive elements should be keyboard accessible
    And all images should have alt text
    And the page should have proper color contrast
    And form elements should have proper labels