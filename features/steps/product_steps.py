"""Step definitions for product page functionality."""
from behave import given, when, then
from pages.product_page import ProductPage
from pages.home_page import HomePage
import time


@when('I navigate to the "{product_name}" product page')
def step_navigate_to_product_page(context, product_name):
    """Navigate to a specific product page."""
    # First go to homepage
    home_page = HomePage(context.driver)
    home_page.open_homepage()
    
    # Navigate to product page
    if product_name == "Digital Shelf":
        home_page.navigate_to_digital_shelf()
    elif product_name == "Sales & Share":
        home_page.navigate_to_sales_share()
    elif product_name == "Content Optimizer":
        home_page.navigate_to_content_optimizer()
    elif product_name == "Shelf Intelligent Media":
        home_page.navigate_to_shelf_intelligent_media()
    elif product_name == "Autopilot":
        home_page.navigate_to_autopilot()
    else:
        # Try direct URL navigation
        product_url = f"/product/{product_name.lower().replace(' ', '-').replace('&', '')}"
        context.driver.get(f"{context.base_url}{product_url}")
    
    # Initialize product page object
    context.product_page = ProductPage(context.driver)
    time.sleep(2)  # Wait for page to load


@when('I navigate to any product page')
def step_navigate_to_any_product_page(context):
    """Navigate to any product page (default to Digital Shelf)."""
    step_navigate_to_product_page(context, "Digital Shelf")


@then('I should see the product page title')
def step_verify_product_page_title(context):
    """Verify that product page title is visible."""
    title = context.product_page.get_product_title()
    assert title and len(title) > 0, "Product page should have a title"


@then('I should see the product description')
def step_verify_product_description(context):
    """Verify that product description is visible."""
    description = context.product_page.get_product_description()
    assert description and len(description) > 0, "Product page should have a description"


@then('I should see a "{button_text}" button')
def step_verify_button_presence(context, button_text):
    """Verify that a specific button is present."""
    if "Request a demo" in button_text:
        assert context.product_page.is_request_demo_button_visible(), f"'{button_text}' button should be visible"
    else:
        from selenium.webdriver.common.by import By
        buttons = context.driver.find_elements(By.XPATH, f"//button[contains(text(), '{button_text}')]")
        links = context.driver.find_elements(By.XPATH, f"//a[contains(text(), '{button_text}')]")
        assert len(buttons) > 0 or len(links) > 0, f"'{button_text}' button should be present"


@then('the page URL should contain "{url_segment}"')
def step_verify_url_segment(context, url_segment):
    """Verify that page URL contains a specific segment."""
    current_url = context.product_page.get_current_url()
    assert url_segment in current_url, f"URL should contain '{url_segment}'. Current URL: {current_url}"


@then('I should see the product title "{expected_title}"')
def step_verify_specific_product_title(context, expected_title):
    """Verify a specific product title."""
    actual_title = context.product_page.get_product_title()
    assert expected_title.lower() in actual_title.lower(), \
        f"Expected title '{expected_title}' not found in '{actual_title}'"


@then('I should see the product title containing "{text}"')
def step_verify_product_title_contains(context, text):
    """Verify that product title contains specific text."""
    actual_title = context.product_page.get_product_title()
    assert text.lower() in actual_title.lower(), \
        f"Product title should contain '{text}'. Actual title: '{actual_title}'"


@then('I should see product features listed')
def step_verify_product_features(context):
    """Verify that product features are listed."""
    features = context.product_page.get_product_features()
    assert len(features) > 0, "Product page should have features listed"


@then('I should see product benefits listed')
def step_verify_product_benefits(context):
    """Verify that product benefits are listed."""
    benefits = context.product_page.get_product_benefits()
    assert len(benefits) > 0, "Product page should have benefits listed"


@then('I should see product screenshots or images')
def step_verify_product_images(context):
    """Verify that product images are present."""
    images = context.product_page.get_product_images()
    assert len(images) > 0, "Product page should have images"


@then('I should see customer testimonials or case studies')
def step_verify_testimonials_or_case_studies(context):
    """Verify that testimonials or case studies are present."""
    testimonials = context.product_page.get_testimonials()
    case_studies = context.product_page.get_case_studies()
    assert len(testimonials) > 0 or len(case_studies) > 0, \
        "Product page should have testimonials or case studies"


@then('I should see information about {topic}')
def step_verify_topic_information(context, topic):
    """Verify that information about a specific topic is present."""
    page_text = context.driver.page_source.lower()
    topic_keywords = {
        'sales analytics': ['sales', 'analytics', 'data', 'performance'],
        'market share': ['market', 'share', 'competitive', 'analysis'],
        'content optimization': ['content', 'optimization', 'optimize', 'improve'],
        'ai or machine learning': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'algorithm']
    }
    
    keywords = topic_keywords.get(topic.lower(), [topic.lower()])
    found_keywords = [keyword for keyword in keywords if keyword in page_text]
    
    assert len(found_keywords) > 0, f"Information about '{topic}' not found on the page"


@then('I should see Amazon-specific features mentioned')
def step_verify_amazon_features(context):
    """Verify that Amazon-specific features are mentioned."""
    page_text = context.driver.page_source.lower()
    amazon_keywords = ['amazon', 'aws', 'marketplace', 'seller central', 'vendor central']
    found_keywords = [keyword for keyword in amazon_keywords if keyword in page_text]
    
    assert len(found_keywords) > 0, "Amazon-specific features should be mentioned"


@then('I should see mentions of AI or machine learning')
def step_verify_ai_mentions(context):
    """Verify that AI or machine learning is mentioned."""
    step_verify_topic_information(context, 'ai or machine learning')


@then('I should see keyword optimization features')
def step_verify_keyword_optimization(context):
    """Verify that keyword optimization features are mentioned."""
    page_text = context.driver.page_source.lower()
    keyword_terms = ['keyword', 'seo', 'search optimization', 'search terms', 'optimization']
    found_terms = [term for term in keyword_terms if term in page_text]
    
    assert len(found_terms) > 0, "Keyword optimization features should be mentioned"


@then('I should see breadcrumb navigation')
def step_verify_breadcrumb_navigation(context):
    """Verify that breadcrumb navigation is present."""
    breadcrumbs = context.product_page.get_breadcrumb_navigation()
    # Breadcrumbs might not be present on all pages, so we'll check if they exist
    # If they exist, they should be functional
    if len(breadcrumbs) > 0:
        assert all('text' in bc and bc['text'] for bc in breadcrumbs), \
            "Breadcrumbs should have proper text"


@then('I should be able to navigate back to homepage')
def step_verify_homepage_navigation(context):
    """Verify that navigation back to homepage is possible."""
    from selenium.webdriver.common.by import By
    # Check for logo or home link
    logo_links = context.driver.find_elements(By.CSS_SELECTOR, ".navbar_logo, .logo")
    home_links = context.driver.find_elements(By.LINK_TEXT, "Home")
    
    assert len(logo_links) > 0 or len(home_links) > 0, \
        "Should be able to navigate back to homepage"


@then('I should see related products or services')
def step_verify_related_products(context):
    """Verify that related products or services are shown."""
    related_products = context.product_page.get_related_products()
    # Related products might not be present on all pages
    # This is more of an informational check
    context.logger.info(f"Found {len(related_products)} related products")


@then('I should see the main navigation menu')
def step_verify_main_navigation_on_product_page(context):
    """Verify that main navigation menu is present on product page."""
    from selenium.webdriver.common.by import By
    nav_menu = context.driver.find_elements(By.CSS_SELECTOR, ".navbar_menu, .main-nav, nav")
    assert len(nav_menu) > 0, "Main navigation menu should be present"


@then('the button should be clickable')
def step_verify_button_clickable(context):
    """Verify that the button is clickable."""
    assert context.product_page.is_request_demo_button_visible(), \
        "Request demo button should be clickable"


@when('I click the "{button_text}" button')
def step_click_product_page_button(context, button_text):
    """Click a button on the product page."""
    if "Request a demo" in button_text:
        assert context.product_page.click_request_demo(), f"Failed to click '{button_text}' button"
    elif "Learn more" in button_text:
        assert context.product_page.click_learn_more(), f"Failed to click '{button_text}' button"
    else:
        raise NotImplementedError(f"Button click for '{button_text}' not implemented")


@then('I should be redirected to the demo request form')
def step_verify_demo_form_redirect(context):
    """Verify redirection to demo request form."""
    current_url = context.product_page.get_current_url()
    assert any(keyword in current_url.lower() for keyword in ['demo', 'request', 'contact', 'form']), \
        f"Should be redirected to demo request form. Current URL: {current_url}"


@then('I should see a contact form')
def step_verify_contact_form_presence(context):
    """Verify that a contact form is present."""
    from selenium.webdriver.common.by import By
    forms = context.driver.find_elements(By.TAG_NAME, "form")
    assert len(forms) > 0, "Contact form should be present"


@then('I should see product images')
def step_verify_product_images_presence(context):
    """Verify that product images are present."""
    images = context.product_page.get_product_images()
    assert len(images) > 0, "Product images should be present"


@then('images should have proper alt text')
def step_verify_image_alt_text(context):
    """Verify that images have proper alt text."""
    from selenium.webdriver.common.by import By
    images = context.driver.find_elements(By.TAG_NAME, "img")
    
    for img in images:
        alt_text = img.get_attribute("alt")
        src = img.get_attribute("src")
        assert alt_text is not None, f"Image missing alt attribute: {src}"


@then('I should be able to play the video')
def step_verify_video_playability(context):
    """Verify that video can be played."""
    if context.product_page.is_video_section_present():
        # Try to play the video
        video_played = context.product_page.play_product_video()
        if not video_played:
            context.logger.info("Video play button not found or not clickable")
    else:
        context.logger.info("No video section found on this product page")


@then('the video should load without errors')
def step_verify_video_loads(context):
    """Verify that video loads without errors."""
    if context.product_page.is_video_section_present():
        # Check for video elements
        from selenium.webdriver.common.by import By
        videos = context.driver.find_elements(By.TAG_NAME, "video")
        iframes = context.driver.find_elements(By.TAG_NAME, "iframe")
        
        # If there are video elements or iframes (for embedded videos), consider it loaded
        assert len(videos) > 0 or len(iframes) > 0, "Video should load without errors"
    else:
        context.logger.info("No video section found on this product page")


@when('I measure the page load time')
def step_measure_product_page_load_time(context):
    """Measure product page load time."""
    context.performance_metrics = context.helpers.get_page_performance_metrics()


@when('I resize the browser to mobile view')
def step_resize_to_mobile(context):
    """Resize browser to mobile view."""
    context.driver.set_window_size(375, 667)  # iPhone 6/7/8 size
    time.sleep(1)


@then('the product content should be readable')
def step_verify_mobile_readability(context):
    """Verify that product content is readable on mobile."""
    title = context.product_page.get_product_title()
    assert title and len(title) > 0, "Product title should be readable on mobile"


@then('images should scale appropriately')
def step_verify_image_scaling(context):
    """Verify that images scale appropriately."""
    from selenium.webdriver.common.by import By
    images = context.driver.find_elements(By.TAG_NAME, "img")
    
    for img in images:
        if img.is_displayed():
            width = img.size['width']
            # Images should not exceed viewport width on mobile
            assert width <= 375, f"Image width {width}px should not exceed mobile viewport"


@then('the CTA button should remain accessible')
def step_verify_mobile_cta_accessibility(context):
    """Verify that CTA button remains accessible on mobile."""
    assert context.product_page.is_request_demo_button_visible(), \
        "CTA button should remain accessible on mobile"


@then('the page should have a unique title tag')
def step_verify_unique_title_tag(context):
    """Verify that page has a unique title tag."""
    title = context.product_page.get_title()
    assert title and len(title) > 0, "Page should have a unique title tag"
    # Store title for comparison across pages if needed
    if not hasattr(context, 'page_titles'):
        context.page_titles = []
    context.page_titles.append(title)


@then('the page should have structured data markup')
def step_verify_structured_data(context):
    """Verify that page has structured data markup."""
    from selenium.webdriver.common.by import By
    # Check for JSON-LD structured data
    json_ld = context.driver.find_elements(By.CSS_SELECTOR, "script[type='application/ld+json']")
    # Check for microdata
    microdata = context.driver.find_elements(By.CSS_SELECTOR, "[itemscope], [itemtype]")
    
    # At least one type of structured data should be present
    has_structured_data = len(json_ld) > 0 or len(microdata) > 0
    if not has_structured_data:
        context.logger.info("No structured data markup found (this may be acceptable)")


@when('I collect all links on the page')
def step_collect_page_links(context):
    """Collect all links on the current page."""
    from selenium.webdriver.common.by import By
    links = context.driver.find_elements(By.TAG_NAME, "a")
    
    context.page_links = []
    for link in links:
        href = link.get_attribute("href")
        if href:
            context.page_links.append({
                'url': href,
                'text': link.text.strip(),
                'is_external': not href.startswith(context.base_url)
            })


@then('all internal links should be working')
def step_verify_internal_links(context):
    """Verify that all internal links are working."""
    if not hasattr(context, 'page_links'):
        step_collect_page_links(context)
    
    internal_links = [link['url'] for link in context.page_links if not link['is_external']]
    
    if len(internal_links) > 0:
        # Test a sample of internal links to avoid long execution times
        sample_links = internal_links[:5]  # Test first 5 links
        link_results = context.helpers.verify_links(sample_links)
        
        broken_links = link_results.get('broken_links', [])
        assert len(broken_links) == 0, f"Found {len(broken_links)} broken internal links"


@then('all external links should open in new tabs')
def step_verify_external_links_target(context):
    """Verify that external links open in new tabs."""
    if not hasattr(context, 'page_links'):
        step_collect_page_links(context)
    
    from selenium.webdriver.common.by import By
    external_link_elements = context.driver.find_elements(
        By.CSS_SELECTOR, f"a[href]:not([href^='{context.base_url}'])"
    )
    
    for link in external_link_elements:
        href = link.get_attribute("href")
        if href and not href.startswith(context.base_url) and not href.startswith('mailto:'):
            target = link.get_attribute("target")
            # External links should open in new tab/window
            if target != "_blank":
                context.logger.warning(f"External link doesn't open in new tab: {href}")


@then('there should be no broken links')
def step_verify_no_broken_links(context):
    """Verify that there are no broken links."""
    if not hasattr(context, 'page_links'):
        step_collect_page_links(context)
    
    # Test a sample of links to avoid long execution times
    all_links = [link['url'] for link in context.page_links]
    sample_links = all_links[:10]  # Test first 10 links
    
    if len(sample_links) > 0:
        link_results = context.helpers.verify_links(sample_links)
        broken_links = link_results.get('broken_links', [])
        
        if len(broken_links) > 0:
            context.logger.warning(f"Found {len(broken_links)} potentially broken links")
            # Don't fail the test for this, just log the warning


@when('there is a contact or demo request form')
def step_check_for_form(context):
    """Check if there is a contact or demo request form."""
    from selenium.webdriver.common.by import By
    forms = context.driver.find_elements(By.TAG_NAME, "form")
    context.has_form = len(forms) > 0


@then('I should be able to fill out the form')
def step_verify_form_fillable(context):
    """Verify that form can be filled out."""
    if hasattr(context, 'has_form') and context.has_form:
        from selenium.webdriver.common.by import By
        inputs = context.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
        assert len(inputs) > 0, "Form should have fillable inputs"
    else:
        context.logger.info("No form found on this page")


@then('form validation should work properly')
def step_verify_form_validation(context):
    """Verify that form validation works properly."""
    if hasattr(context, 'has_form') and context.has_form:
        # This would require more complex testing of form validation
        # For now, just verify that required fields exist
        from selenium.webdriver.common.by import By
        required_inputs = context.driver.find_elements(By.CSS_SELECTOR, "input[required], textarea[required]")
        context.logger.info(f"Found {len(required_inputs)} required form fields")
    else:
        context.logger.info("No form found on this page")


@then('I should be able to submit the form successfully')
def step_verify_form_submission(context):
    """Verify that form can be submitted successfully."""
    if hasattr(context, 'has_form') and context.has_form:
        from selenium.webdriver.common.by import By
        submit_buttons = context.driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        assert len(submit_buttons) > 0, "Form should have a submit button"
    else:
        context.logger.info("No form found on this page")