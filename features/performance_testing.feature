Feature: Performance Testing
  As a QA engineer
  I want to test the performance of the Profitero website
  So that I can ensure optimal user experience

  @performance @load_time
  Scenario: Page load time performance
    Given I am measuring website performance
    When I load the homepage
    Then the page should load in less than 3 seconds
    And the DOM should be ready in less than 2 seconds
    And all critical resources should load quickly

  @performance @page_size
  Scenario: Page size optimization
    Given I am analyzing page resources
    When I measure page sizes
    Then the homepage should be under 2MB total size
    And images should be optimized for web
    And CSS and JavaScript should be minified
    And unnecessary resources should be eliminated

  @performance @caching
  Scenario: Caching mechanisms
    Given I am testing caching behavior
    When I visit pages multiple times
    Then static resources should be cached properly
    And cache headers should be set appropriately
    And subsequent page loads should be faster

  @performance @image_optimization
  Scenario: Image optimization
    Given I am analyzing image performance
    When I inspect all images on the website
    Then images should be in appropriate formats (WebP, JPEG, PNG)
    And images should have appropriate dimensions
    And lazy loading should be implemented where appropriate
    And images should have proper compression

  @performance @javascript
  Scenario: JavaScript performance
    Given I am testing JavaScript performance
    When I analyze JavaScript execution
    Then JavaScript should not block page rendering
    And critical JavaScript should load first
    And non-critical JavaScript should be deferred
    And there should be no memory leaks

  @performance @css
  Scenario: CSS performance
    Given I am testing CSS performance
    When I analyze CSS loading
    Then critical CSS should be inlined or loaded first
    And unused CSS should be removed
    And CSS should be minified
    And render-blocking CSS should be minimized

  @performance @mobile
  Scenario: Mobile performance
    Given I am testing on mobile devices
    When I measure mobile performance
    Then pages should load quickly on 3G connections
    And touch interactions should be responsive
    And mobile-specific optimizations should be present

  @performance @core_web_vitals
  Scenario: Core Web Vitals metrics
    Given I am measuring Core Web Vitals
    When I analyze the website performance
    Then Largest Contentful Paint (LCP) should be under 2.5 seconds
    And First Input Delay (FID) should be under 100 milliseconds
    And Cumulative Layout Shift (CLS) should be under 0.1

  @performance @network
  Scenario: Network performance optimization
    Given I am testing network performance
    When I analyze network requests
    Then HTTP/2 should be used where possible
    And requests should be minimized through bundling
    And CDN should be used for static resources
    And compression should be enabled (gzip/brotli)

  @performance @database
  Scenario: Database performance (if applicable)
    Given I am testing database-dependent features
    When I measure database query performance
    Then database queries should execute quickly
    And there should be no N+1 query problems
    And database connections should be properly managed

  @performance @concurrent_users
  Scenario: Concurrent user handling
    Given I am testing with multiple concurrent users
    When I simulate multiple users accessing the website
    Then the website should handle concurrent load gracefully
    And response times should remain acceptable
    And there should be no server errors under load

  @performance @memory_usage
  Scenario: Memory usage optimization
    Given I am monitoring memory usage
    When I use the website extensively
    Then memory usage should remain stable
    And there should be no memory leaks
    And garbage collection should work efficiently

  @performance @third_party
  Scenario: Third-party service performance
    Given the website uses third-party services
    When I analyze third-party impact
    Then third-party scripts should not significantly impact performance
    And third-party resources should load asynchronously
    And fallbacks should exist for third-party failures

  @performance @api_performance
  Scenario: API performance
    Given I am testing API performance
    When I measure API response times
    Then API calls should respond within acceptable time limits
    And API should handle concurrent requests efficiently
    And API responses should be properly cached where appropriate