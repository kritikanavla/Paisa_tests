import sys
import os
import random
import string
import time
from playwright.sync_api import sync_playwright

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + "@example.com"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url="https://paisa.example.com")
        page = context.new_page()
        
        email = random_email()
        password = "Password123!"
        
        print(f"1. Navigating to login page...")
        page.goto("/login")
        page.screenshot(path="step1_login.png")
        
        print(f"2. Switching to Register tab...")
        page.click("button:has-text('Register')")
        page.wait_for_timeout(1000)
        page.screenshot(path="step2_register_tab.png")
        
        print(f"3. Filling registration form ({email})...")
        page.fill("id=email", email)
        page.fill("id=password", password)
        page.screenshot(path="step3_filled.png")
        
        print("4. Clicking Sign Up...")
        # Use the specific locator we found earlier
        page.click("button[type='submit']:has-text('Sign Up')")
        
        print("5. Waiting for Dashboard...")
        try:
            page.wait_for_url("**/dashboard", timeout=30000)
            print("Successfully reached Dashboard!")
            page.screenshot(path="step5_dashboard.png")
            
            print("6. Clicking 'Record New Trade'...")
            page.click("button:has-text('Record New Trade')")
            page.wait_for_timeout(2000)
            page.screenshot(path="step6_trade_form.png")
            
            print("7. Extracting form data...")
            form = page.query_selector("form")
            if form:
                print("Form found!")
                fields = form.query_selector_all("input, select, textarea, button")
                for field in fields:
                    tag = field.evaluate("el => el.tagName")
                    id_attr = field.get_attribute("id")
                    name_attr = field.get_attribute("name")
                    type_attr = field.get_attribute("type")
                    placeholder = field.get_attribute("placeholder")
                    label = page.query_selector(f"label[for='{id_attr}']") if id_attr else None
                    label_text = label.inner_text() if label else "N/A"
                    print(f"Field: Tag={tag}, Label={label_text}, ID={id_attr}, Name={name_attr}, Type={type_attr}, Placeholder={placeholder}")
            else:
                print("Form NOT found on dashboard.")
                # Maybe it's a modal?
                modals = page.query_selector_all("[role='dialog'], .modal, .popup")
                print(f"Found {len(modals)} potential modals.")
                for i, modal in enumerate(modals):
                    print(f"Modal {i} content: {modal.inner_text()[:100]}...")
            
        except Exception as e:
            print(f"Failed to reach dashboard or find form: {e}")
            page.screenshot(path="error_final.png")
            with open("final_content.html", "w") as f:
                f.write(page.content())
        
        browser.close()

if __name__ == "__main__":
    run()

