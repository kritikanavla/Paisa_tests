import sys
import os
import random
import string
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
        
        print(f"Registering with {email}...")
        page.goto("/login")
        page.click("button:has-text('Register')")
        page.fill("id=email", email)
        page.fill("id=password", password)
        page.click("button:has-text('Sign Up')")
        
        page.wait_for_url("**/dashboard", timeout=20000)
        print("Registered and logged in successfully.")
        
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
        print("Screenshot saved to trade_form.png")
        
        browser.close()

if __name__ == "__main__":
    run()

