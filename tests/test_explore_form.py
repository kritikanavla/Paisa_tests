import pytest
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage

def test_explore_trade_form(logged_in_dashboard: DashboardPage):
    page = logged_in_dashboard.page
    print(f"Current URL: {page.url}")
    
    # Click Record Trade
    logged_in_dashboard.record_trade_btn.click()
    
    # Wait for the form
    page.wait_for_selector("form", timeout=10000)
    
    # Extract all labels and input types
    labels = page.query_selector_all("label")
    for label in labels:
        for_id = label.get_attribute("for")
        text = label.inner_text()
        print(f"Label: {text}, For ID: {for_id}")
        if for_id:
            input_el = page.query_selector(f"#{for_id}")
            if input_el:
                tag = input_el.evaluate("el => el.tagName")
                type_attr = input_el.get_attribute("type")
                print(f"  Input: Tag={tag}, Type={type_attr}")
    
    # Also look for select boxes
    selects = page.query_selector_all("select")
    for select in selects:
        id_attr = select.get_attribute("id")
        name_attr = select.get_attribute("name")
        print(f"Select: ID={id_attr}, Name={name_attr}")
        options = select.query_selector_all("option")
        opt_texts = [opt.inner_text() for opt in options]
        print(f"  Options: {opt_texts}")

    page.screenshot(path="trade_form_final.png")
