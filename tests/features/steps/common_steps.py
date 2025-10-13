from behave import given, when, then
import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.utils.driver_factory import build_webdriver
from tests.utils.base_page import BasePage


@given("I launch the browser")
def step_launch_browser(context):
    context.driver = build_webdriver(
        browser=context.browser,
        headless=context.headless,
        pageload_timeout=context.pageload_timeout,
        implicit_wait=context.implicit_wait,
    )
    context.page = BasePage(context.driver, context.base_url)


def _teardown_driver(context):
    driver = getattr(context, "driver", None)
    if driver:
        try:
            driver.quit()
        except Exception:
            pass


# driver teardown is handled in environment hooks


@when('I open path "{path}"')
def step_open_path(context, path):
    context.page.open(path)


@then('I should see text containing "{text}"')
def step_see_text(context, text):
    WebDriverWait(context.driver, context.explicit_wait).until(
        EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(., '{text}')]"))
    )


@then('the element "{css}" should exist')
def step_element_exists(context, css):
    elements = context.driver.find_elements(By.CSS_SELECTOR, css)
    assert elements, f"Element not found for CSS: {css}"


@then('the mobile menu toggle should be present if applicable')
def step_mobile_toggle(context):
    # This is a generic check; site may vary
    selectors = [
        'button[aria-label*="menu" i]',
        'button[aria-expanded]',
        'button.menu',
        '.hamburger',
    ]
    found = any(context.driver.find_elements(By.CSS_SELECTOR, sel) for sel in selectors)
    assert found, "No mobile menu toggle found with common selectors"


# API steps
@when('I GET "{path}"')
def step_api_get(context, path):
    url = urljoin(context.base_url, path)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    context.api_response = requests.get(url, timeout=context.request_timeout, headers=headers)


@then('the response status should be {status:d}')
def step_status_should_be(context, status):
    assert context.api_response.status_code == status, f"Expected {status}, got {context.api_response.status_code}"


@then('the response body should contain "{needle}"')
def step_body_contains(context, needle):
    assert needle in context.api_response.text


@then('the response body should not be empty')
def step_body_not_empty(context):
    body = context.api_response.text or ""
    assert len(body.strip()) > 0, "Expected non-empty response body"


# Scraping steps
@given("I plan to scrape these paths")
def step_plan_scrape(context):
    context.scrape_paths = [row["path"].strip() for row in context.table]


@when("I scrape the pages")
def step_scrape_pages(context):
    results = []
    for path in context.scrape_paths:
        url = urljoin(context.base_url, path)
        resp = requests.get(url, timeout=context.request_timeout, headers={"User-Agent": "SEO-Scraper/1.0"})
        soup = BeautifulSoup(resp.text, "lxml")
        title = (soup.title.string or "").strip() if soup.title else ""
        h1 = " | ".join([h.get_text(strip=True) for h in soup.find_all("h1")])
        h2 = " | ".join([h.get_text(strip=True) for h in soup.find_all("h2")])
        h3 = " | ".join([h.get_text(strip=True) for h in soup.find_all("h3")])
        canonical_tag = soup.find("link", rel=lambda v: v and "canonical" in v)
        canonical = canonical_tag.get("href") if canonical_tag else ""
        results.append({
            "url": url,
            "title": title,
            "h1": h1,
            "h2": h2,
            "h3": h3,
            "canonical": canonical,
        })
    context.scrape_results = results


@then('I export the results to "{outfile}"')
def step_export_results(context, outfile):
    path = outfile
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "title", "h1", "h2", "h3", "canonical"])
        writer.writeheader()
        writer.writerows(context.scrape_results)
