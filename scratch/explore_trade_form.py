import sys
import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url="https://paisa.example.com")
        page = context.new_page()
        
        print("Navigating to login page...")
        page.goto("/login")
        
        print("Logging in...")
        page.fill("id=email", "test@example.com")
        page.fill("id=password", "Password123!")
        page.click("button:has-text('Sign In')")
        
        # Wait a bit and take a screenshot
        page.wait_for_timeout(5000)
        page.screenshot(path="login_result.png")
        print(f"Current URL: {page.url}")
        
        if "/dashboard" in page.url:
            print("Logged in successfully.")
            print("Opening 'Record New Trade' form...")
            page.click("button:has-text('Record New Trade')")
            page.wait_for_selector("form", timeout=10000)
            
            print("Form found. Extracting fields...")
            fields = page.query_selector_all("form input, form select, form textarea")
            for field in fields:
                name = field.get_attribute("name")
                id = field.get_attribute("id")
                placeholder = field.get_attribute("placeholder")
                type = field.get_attribute("type")
                label_text = ""
                if id:
                    label = page.query_selector(f"label[for='{id}']")
                    if label:
                        label_text = label.inner_text()
                
                print(f"Field: Label='{label_text}', Name='{name}', ID='{id}', Placeholder='{placeholder}', Type='{type}'")
            
            page.screenshot(path="trade_form.png")
        else:
            print("Failed to login or redirected elsewhere.")
            # Check for error messages
            error = page.query_selector("text=Invalid email or password")
            if error:
                print(f"Error message: {error.inner_text()}")
        
        browser.close()

if __name__ == "__main__":
    run()

