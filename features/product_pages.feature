Feature: Product Pages Functionality
  As a potential customer
  I want to explore product pages
  So that I can understand the features and benefits of each product

  Background:
    Given I am on the Profitero homepage

  @smoke @products
  Scenario Outline: Product page loads successfully
    When I navigate to the "<product_name>" product page
    Then I should see the product page title
    And I should see the product description
    And I should see a "Request a demo" button
    And the page URL should contain "<url_segment>"

    Examples:
      | product_name              | url_segment           |
      | Digital Shelf             | digital-shelf         |
      | Sales & Share             | sales-share           |
      | Content Optimizer         | content-optimizer     |
      | Shelf Intelligent Media   | shelf-intelligent-media |
      | Autopilot                 | autopilot             |

  @products @content
  Scenario: Digital Shelf product page content
    When I navigate to the "Digital Shelf" product page
    Then I should see the product title "Digital Shelf"
    And I should see product features listed
    And I should see product benefits listed
    And I should see product screenshots or images
    And I should see customer testimonials or case studies

  @products @content
  Scenario: Sales & Share product page content
    When I navigate to the "Sales & Share" product page
    Then I should see the product title containing "Sales"
    And I should see information about sales analytics
    And I should see information about market share
    And I should see Amazon-specific features mentioned

  @products @content
  Scenario: Content Optimizer product page content
    When I navigate to the "Content Optimizer" product page
    Then I should see the product title "Content Optimizer"
    And I should see information about content optimization
    And I should see mentions of AI or machine learning
    And I should see keyword optimization features

  @products @navigation
  Scenario: Product page navigation elements
    When I navigate to any product page
    Then I should see breadcrumb navigation
    And I should be able to navigate back to homepage
    And I should see related products or services
    And I should see the main navigation menu

  @products @cta
  Scenario: Product page call-to-action buttons
    When I navigate to any product page
    Then I should see a "Request a demo" button
    And the button should be clickable
    When I click the "Request a demo" button
    Then I should be redirected to the demo request form
    Or I should see a contact form

  @products @media
  Scenario: Product page multimedia content
    When I navigate to any product page
    Then I should see product images
    And images should have proper alt text
    If there is a video section
    Then I should be able to play the video
    And the video should load without errors

  @products @performance
  Scenario: Product pages load performance
    When I navigate to any product page
    And I measure the page load time
    Then the page should load in less than 5 seconds
    And there should be no JavaScript console errors
    And all images should load successfully

  @products @responsive
  Scenario: Product pages are responsive
    When I navigate to any product page
    And I resize the browser to mobile view
    Then the product content should be readable
    And images should scale appropriately
    And the CTA button should remain accessible

  @products @seo
  Scenario: Product pages have proper SEO
    When I navigate to any product page
    Then the page should have a unique title tag
    And the page should have a meta description
    And the page should have proper heading hierarchy
    And the page should have structured data markup

  @products @links
  Scenario: Product page links are functional
    When I navigate to any product page
    And I collect all links on the page
    Then all internal links should be working
    And all external links should open in new tabs
    And there should be no broken links

  @products @forms
  Scenario: Product page forms work correctly
    When I navigate to any product page
    And there is a contact or demo request form
    Then I should be able to fill out the form
    And form validation should work properly
    And I should be able to submit the form successfully