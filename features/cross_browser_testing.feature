Feature: Cross Browser Testing
  As a QA engineer
  I want to test the Profitero website across different browsers
  So that I can ensure consistent functionality and appearance

  @cross_browser @chrome
  Scenario: Website functionality in Chrome
    Given I am using Chrome browser
    When I navigate to the Profitero homepage
    Then the website should load correctly
    And all interactive elements should work
    And the layout should render properly
    And JavaScript functionality should work

  @cross_browser @firefox
  Scenario: Website functionality in Firefox
    Given I am using Firefox browser
    When I navigate to the Profitero homepage
    Then the website should load correctly
    And all interactive elements should work
    And the layout should render properly
    And JavaScript functionality should work

  @cross_browser @edge
  Scenario: Website functionality in Edge
    Given I am using Edge browser
    When I navigate to the Profitero homepage
    Then the website should load correctly
    And all interactive elements should work
    And the layout should render properly
    And JavaScript functionality should work

  @cross_browser @safari
  Scenario: Website functionality in Safari
    Given I am using Safari browser
    When I navigate to the Profitero homepage
    Then the website should load correctly
    And all interactive elements should work
    And the layout should render properly
    And JavaScript functionality should work

  @cross_browser @forms
  Scenario Outline: Contact form works across browsers
    Given I am using "<browser>" browser
    When I navigate to the contact page
    And I fill out the contact form
    And I submit the form
    Then the form should submit successfully
    And I should see appropriate feedback

    Examples:
      | browser |
      | Chrome  |
      | Firefox |
      | Edge    |

  @cross_browser @navigation
  Scenario Outline: Navigation works across browsers
    Given I am using "<browser>" browser
    When I test the main navigation menu
    Then all dropdown menus should work
    And all links should be clickable
    And page transitions should be smooth

    Examples:
      | browser |
      | Chrome  |
      | Firefox |
      | Edge    |

  @cross_browser @responsive
  Scenario Outline: Responsive design works across browsers
    Given I am using "<browser>" browser
    When I test different screen sizes
    Then the layout should adapt appropriately
    And content should remain accessible
    And functionality should be preserved

    Examples:
      | browser |
      | Chrome  |
      | Firefox |
      | Edge    |

  @cross_browser @performance
  Scenario Outline: Performance consistency across browsers
    Given I am using "<browser>" browser
    When I measure page load times
    Then pages should load within acceptable time limits
    And there should be no browser-specific performance issues

    Examples:
      | browser |
      | Chrome  |
      | Firefox |
      | Edge    |

  @cross_browser @css
  Scenario Outline: CSS rendering consistency
    Given I am using "<browser>" browser
    When I inspect the visual appearance
    Then fonts should render correctly
    And colors should display accurately
    And layouts should be consistent
    And animations should work smoothly

    Examples:
      | browser |
      | Chrome  |
      | Firefox |
      | Edge    |

  @cross_browser @javascript
  Scenario Outline: JavaScript compatibility
    Given I am using "<browser>" browser
    When I test JavaScript functionality
    Then all interactive features should work
    And there should be no console errors
    And event handlers should function properly

    Examples:
      | browser |
      | Chrome  |
      | Firefox |
      | Edge    |