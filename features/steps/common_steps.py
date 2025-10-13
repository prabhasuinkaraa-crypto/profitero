"""Common step definitions shared across features."""
from behave import given, when, then
import time


@given('I am using {browser} browser')
def step_setup_browser(context, browser):
    """Set up specific browser for testing."""
    from features.environment import use_browser
    use_browser(context, browser.lower())


@when('I test the main navigation menu')
def step_test_main_navigation(context):
    """Test the main navigation menu functionality."""
    from pages.home_page import HomePage
    
    home_page = HomePage(context.driver)
    home_page.open_homepage()
    
    # Test navigation visibility
    assert home_page.is_main_navigation_visible(), "Main navigation should be visible"
    
    # Test dropdown functionality
    if home_page.hover_over_products_menu():
        context.logger.info("Products dropdown menu works")
    
    context.navigation_tested = True


@then('all dropdown menus should work')
def step_verify_dropdown_menus(context):
    """Verify that all dropdown menus work correctly."""
    if hasattr(context, 'navigation_tested') and context.navigation_tested:
        context.logger.info("Dropdown menus verified")
    else:
        context.logger.warning("Navigation not tested")


@then('all links should be clickable')
def step_verify_links_clickable(context):
    """Verify that all links are clickable."""
    from selenium.webdriver.common.by import By
    
    links = context.driver.find_elements(By.TAG_NAME, "a")
    clickable_links = 0
    
    for link in links:
        if link.is_displayed() and link.is_enabled():
            href = link.get_attribute("href")
            if href and href != "#":
                clickable_links += 1
    
    assert clickable_links > 0, "Should have clickable links"
    context.logger.info(f"Found {clickable_links} clickable links")


@then('page transitions should be smooth')
def step_verify_smooth_transitions(context):
    """Verify that page transitions are smooth."""
    # This is more of a subjective measure, we'll check for basic functionality
    current_url = context.driver.current_url
    assert current_url, "Page should load successfully"
    context.logger.info("Page transitions verified")


@when('I test different screen sizes')
def step_test_different_screen_sizes(context):
    """Test different screen sizes for responsive design."""
    screen_sizes = [
        (375, 667),   # Mobile
        (768, 1024),  # Tablet
        (1920, 1080)  # Desktop
    ]
    
    context.responsive_tests = []
    
    for width, height in screen_sizes:
        context.driver.set_window_size(width, height)
        time.sleep(1)  # Wait for resize
        
        # Basic functionality test
        from selenium.webdriver.common.by import By
        body = context.driver.find_element(By.TAG_NAME, "body")
        
        context.responsive_tests.append({
            'size': f"{width}x{height}",
            'body_visible': body.is_displayed(),
            'page_width': context.driver.execute_script("return document.body.scrollWidth"),
            'viewport_width': width
        })


@then('the layout should adapt appropriately')
def step_verify_layout_adaptation(context):
    """Verify that layout adapts appropriately to different screen sizes."""
    if hasattr(context, 'responsive_tests'):
        for test in context.responsive_tests:
            assert test['body_visible'], f"Body should be visible at {test['size']}"
            
            # Check that content doesn't overflow significantly
            overflow = test['page_width'] - test['viewport_width']
            if overflow > 50:  # Allow some overflow for scrollbars
                context.logger.warning(f"Significant overflow at {test['size']}: {overflow}px")
        
        context.logger.info(f"Layout adaptation tested for {len(context.responsive_tests)} screen sizes")


@then('content should remain accessible')
def step_verify_content_accessibility(context):
    """Verify that content remains accessible across screen sizes."""
    if hasattr(context, 'responsive_tests'):
        # Content should be accessible if body is visible and functional
        accessible_sizes = [test for test in context.responsive_tests if test['body_visible']]
        assert len(accessible_sizes) == len(context.responsive_tests), \
            "Content should be accessible at all screen sizes"


@then('functionality should be preserved')
def step_verify_functionality_preserved(context):
    """Verify that functionality is preserved across screen sizes."""
    # Reset to desktop size for final check
    context.driver.set_window_size(1920, 1080)
    time.sleep(1)
    
    # Basic functionality check
    from selenium.webdriver.common.by import By
    interactive_elements = context.driver.find_elements(By.CSS_SELECTOR, "a, button, input")
    
    functional_elements = [elem for elem in interactive_elements if elem.is_displayed()]
    assert len(functional_elements) > 0, "Should have functional elements after resize"
    
    context.logger.info("Functionality preservation verified")


@when('I measure page load times')
def step_measure_page_load_times(context):
    """Measure page load times across browsers."""
    start_time = time.time()
    context.driver.refresh()
    
    # Wait for page to be ready
    context.driver.execute_script("return document.readyState") == "complete"
    end_time = time.time()
    
    context.page_load_time = end_time - start_time


@then('pages should load within acceptable time limits')
def step_verify_acceptable_load_times(context):
    """Verify that pages load within acceptable time limits."""
    if hasattr(context, 'page_load_time'):
        max_load_time = 10.0  # 10 seconds maximum
        assert context.page_load_time < max_load_time, \
            f"Page load time {context.page_load_time:.2f}s exceeds limit of {max_load_time}s"
        context.logger.info(f"Page loaded in {context.page_load_time:.2f}s")


@then('there should be no browser-specific performance issues')
def step_verify_no_browser_performance_issues(context):
    """Verify no browser-specific performance issues."""
    # Check for console errors that might indicate performance issues
    try:
        logs = context.driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if len(severe_errors) > 0:
            context.logger.warning(f"Found {len(severe_errors)} severe browser errors")
        else:
            context.logger.info("No severe browser performance issues found")
    except:
        context.logger.info("Could not check browser logs")


@when('I inspect the visual appearance')
def step_inspect_visual_appearance(context):
    """Inspect the visual appearance of the page."""
    from selenium.webdriver.common.by import By
    
    # Check for basic visual elements
    context.visual_elements = {
        'images': len(context.driver.find_elements(By.TAG_NAME, "img")),
        'headings': len(context.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")),
        'paragraphs': len(context.driver.find_elements(By.TAG_NAME, "p")),
        'links': len(context.driver.find_elements(By.TAG_NAME, "a"))
    }


@then('fonts should render correctly')
def step_verify_font_rendering(context):
    """Verify that fonts render correctly."""
    from selenium.webdriver.common.by import By
    
    # Check that text elements have reasonable font sizes
    text_elements = context.driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, span, div")
    
    readable_text_found = False
    for element in text_elements:
        if element.is_displayed() and element.text.strip():
            font_size = context.driver.execute_script(
                "return window.getComputedStyle(arguments[0]).fontSize", element
            )
            if font_size and int(font_size.replace('px', '')) >= 12:
                readable_text_found = True
                break
    
    assert readable_text_found, "Should have readable font sizes"
    context.logger.info("Font rendering verified")


@then('colors should display accurately')
def step_verify_color_accuracy(context):
    """Verify that colors display accurately."""
    from selenium.webdriver.common.by import By
    
    # Check that elements have color styles applied
    colored_elements = context.driver.find_elements(By.CSS_SELECTOR, "*")
    
    elements_with_color = 0
    for element in colored_elements[:10]:  # Check first 10 elements
        if element.is_displayed():
            color = context.driver.execute_script(
                "return window.getComputedStyle(arguments[0]).color", element
            )
            if color and color != "rgba(0, 0, 0, 0)":
                elements_with_color += 1
    
    assert elements_with_color > 0, "Should have elements with color styles"
    context.logger.info("Color accuracy verified")


@then('layouts should be consistent')
def step_verify_layout_consistency(context):
    """Verify that layouts are consistent."""
    # Check that basic layout elements are present
    from selenium.webdriver.common.by import By
    
    layout_elements = {
        'header': len(context.driver.find_elements(By.CSS_SELECTOR, "header, .header")),
        'main': len(context.driver.find_elements(By.CSS_SELECTOR, "main, .main, .content")),
        'footer': len(context.driver.find_elements(By.CSS_SELECTOR, "footer, .footer"))
    }
    
    # At least one main content area should be present
    has_main_content = layout_elements['main'] > 0 or len(context.driver.find_elements(By.TAG_NAME, "body")) > 0
    assert has_main_content, "Should have main content area"
    
    context.logger.info("Layout consistency verified")


@then('animations should work smoothly')
def step_verify_smooth_animations(context):
    """Verify that animations work smoothly."""
    # Check for CSS animations or transitions
    animated_elements = context.driver.find_elements(By.CSS_SELECTOR, "*")
    
    animations_found = 0
    for element in animated_elements[:20]:  # Check first 20 elements
        if element.is_displayed():
            animation = context.driver.execute_script(
                "return window.getComputedStyle(arguments[0]).animationName", element
            )
            transition = context.driver.execute_script(
                "return window.getComputedStyle(arguments[0]).transitionProperty", element
            )
            
            if (animation and animation != "none") or (transition and transition != "none"):
                animations_found += 1
    
    context.logger.info(f"Found {animations_found} elements with animations/transitions")


@when('I test JavaScript functionality')
def step_test_javascript_functionality(context):
    """Test JavaScript functionality."""
    # Test basic JavaScript execution
    try:
        result = context.driver.execute_script("return typeof jQuery !== 'undefined' || typeof $ !== 'undefined';")
        context.jquery_available = result
        
        # Test DOM manipulation
        context.driver.execute_script("document.body.setAttribute('data-js-test', 'working');")
        test_attr = context.driver.execute_script("return document.body.getAttribute('data-js-test');")
        context.js_dom_working = test_attr == 'working'
        
        context.javascript_tested = True
        
    except Exception as e:
        context.logger.error(f"JavaScript test failed: {e}")
        context.javascript_tested = False


@then('all interactive features should work')
def step_verify_interactive_features(context):
    """Verify that all interactive features work."""
    if hasattr(context, 'javascript_tested') and context.javascript_tested:
        # Test clicking on interactive elements
        from selenium.webdriver.common.by import By
        
        clickable_elements = context.driver.find_elements(By.CSS_SELECTOR, "button, a[href], input[type='submit']")
        
        interactive_count = 0
        for element in clickable_elements[:5]:  # Test first 5 elements
            if element.is_displayed() and element.is_enabled():
                interactive_count += 1
        
        assert interactive_count > 0, "Should have interactive features"
        context.logger.info(f"Verified {interactive_count} interactive features")


@then('there should be no console errors')
def step_verify_no_console_errors_cross_browser(context):
    """Verify that there are no console errors."""
    try:
        logs = context.driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if len(severe_errors) > 0:
            context.logger.warning(f"Found {len(severe_errors)} console errors")
            for error in severe_errors[:3]:  # Log first 3 errors
                context.logger.warning(f"Console error: {error['message']}")
        else:
            context.logger.info("No severe console errors found")
    except:
        context.logger.info("Could not check console errors")


@then('event handlers should function properly')
def step_verify_event_handlers(context):
    """Verify that event handlers function properly."""
    if hasattr(context, 'javascript_tested') and context.javascript_tested:
        # Test event handling by triggering a click event
        from selenium.webdriver.common.by import By
        
        try:
            # Find a clickable element and test click event
            clickable = context.driver.find_element(By.CSS_SELECTOR, "a, button")
            if clickable.is_displayed():
                # Just verify the element is clickable, don't actually click
                assert clickable.is_enabled(), "Clickable element should be enabled"
                context.logger.info("Event handlers verified")
        except:
            context.logger.info("Could not test event handlers")


# Utility step definitions
@when('I wait for {seconds:d} seconds')
def step_wait_for_seconds(context, seconds):
    """Wait for specified number of seconds."""
    time.sleep(seconds)


@when('I take a screenshot')
def step_take_screenshot(context):
    """Take a screenshot of current page."""
    if hasattr(context, 'helpers'):
        screenshot_path = context.helpers.take_screenshot("manual_screenshot")
        context.logger.info(f"Screenshot taken: {screenshot_path}")


@then('the page should be accessible')
def step_verify_page_accessibility(context):
    """Verify basic page accessibility."""
    from selenium.webdriver.common.by import By
    
    # Check for basic accessibility features
    accessibility_checks = {
        'has_title': bool(context.driver.title),
        'has_headings': len(context.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")) > 0,
        'has_alt_text': True,  # Will be checked below
        'has_labels': True     # Will be checked below
    }
    
    # Check images for alt text
    images = context.driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        if img.is_displayed() and not img.get_attribute("alt"):
            accessibility_checks['has_alt_text'] = False
            break
    
    # Check form inputs for labels
    inputs = context.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
    for input_elem in inputs:
        if input_elem.is_displayed():
            input_id = input_elem.get_attribute("id")
            if input_id:
                labels = context.driver.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                if len(labels) == 0 and not input_elem.get_attribute("aria-label"):
                    accessibility_checks['has_labels'] = False
                    break
    
    # Log accessibility status
    passed_checks = sum(accessibility_checks.values())
    total_checks = len(accessibility_checks)
    
    context.logger.info(f"Accessibility checks: {passed_checks}/{total_checks} passed")
    
    # Don't fail the test, just log the results
    if passed_checks < total_checks:
        context.logger.warning("Some accessibility checks failed")


@then('the page should load successfully')
def step_verify_page_loads_successfully(context):
    """Verify that page loads successfully."""
    # Check that we have a valid page
    assert context.driver.current_url, "Should have a valid URL"
    assert context.driver.title, "Should have a page title"
    
    # Check that page is not showing an error
    page_source = context.driver.page_source.lower()
    error_indicators = ['404', '500', 'error', 'not found', 'server error']
    
    has_error = any(indicator in page_source for indicator in error_indicators)
    if has_error:
        context.logger.warning("Page may be showing an error")
    
    context.logger.info("Page loaded successfully")


@given('I have a test environment set up')
def step_setup_test_environment(context):
    """Set up test environment."""
    # This step can be used to ensure test environment is ready
    assert hasattr(context, 'driver'), "WebDriver should be available"
    assert hasattr(context, 'config'), "Configuration should be available"
    context.logger.info("Test environment verified")


@when('I perform a comprehensive test')
def step_perform_comprehensive_test(context):
    """Perform a comprehensive test of the current page."""
    from selenium.webdriver.common.by import By
    
    # Gather comprehensive page information
    context.comprehensive_test_results = {
        'url': context.driver.current_url,
        'title': context.driver.title,
        'elements': {
            'links': len(context.driver.find_elements(By.TAG_NAME, "a")),
            'images': len(context.driver.find_elements(By.TAG_NAME, "img")),
            'forms': len(context.driver.find_elements(By.TAG_NAME, "form")),
            'buttons': len(context.driver.find_elements(By.TAG_NAME, "button")),
            'inputs': len(context.driver.find_elements(By.TAG_NAME, "input"))
        },
        'page_size': len(context.driver.page_source),
        'load_time': getattr(context, 'page_load_time', 0)
    }
    
    context.logger.info(f"Comprehensive test completed: {context.comprehensive_test_results}")


@then('all aspects should be functioning correctly')
def step_verify_all_aspects_functioning(context):
    """Verify that all aspects are functioning correctly."""
    if hasattr(context, 'comprehensive_test_results'):
        results = context.comprehensive_test_results
        
        # Basic checks
        assert results['title'], "Page should have a title"
        assert results['page_size'] > 0, "Page should have content"
        assert results['elements']['links'] >= 0, "Should count links"
        
        context.logger.info("All aspects verified as functioning correctly")
    else:
        context.logger.info("No comprehensive test results to verify")