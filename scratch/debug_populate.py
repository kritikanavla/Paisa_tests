import json
import os
import time
from playwright.sync_api import sync_playwright

# Configuration - update these with real credentials
EMAIL = "test_user_a@example.com"
PASSWORD = "Password123!"
BASE_URL = "https://paisa.example.com"

def debug_populate():
    with open(r"C:\\Users\\USER\.gemini\antigravity\scratch\Paisa tests\trade_data.json", "r") as f:
        trades = json.load(f)[:2] # Only first 2 trades

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        print(f"Logging into {BASE_URL}...")
        page.goto("/login")
        page.type("id=email", EMAIL, delay=50)
        page.type("id=password", PASSWORD, delay=50)
        page.click("button[type='submit']:has-text('Sign In')")

        try:
            page.wait_for_selector("button:has-text('Record New Trade')", timeout=30000)
            print("Successfully logged in.")
            
            # Close guide
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Login failed: {e}")
            page.screenshot(path="debug_login_failure.png")
            with open("debug_login_failure.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            browser.close()
            return

        for trade in trades:
            print(f"Recording trade for {trade['ticker']}...")
            try:
                page.click("button:has-text('Record New Trade')", timeout=10000)
                page.wait_for_selector("form", timeout=5000)
                
                page.fill("input[name='ticker']", trade['ticker'])
                page.fill("input[name='date']", trade['date'])
                
                # Use value for select
                page.select_option("select[name='action']", label=trade['action'])
                
                page.fill("input[name='quantity']", str(trade['quantity']))
                page.fill("input[name='price']", str(trade['price']))
                
                if page.query_selector("input[name='strategy']"):
                    page.fill("input[name='strategy']", trade['strategy'])

                page.click("button[type='submit']")
                page.wait_for_timeout(2000)
                print(f"Done with {trade['ticker']}.")
            except Exception as e:
                print(f"Failed for {trade['ticker']}: {e}")
                page.screenshot(path=f"debug_{trade['ticker']}.png")
        
        browser.close()

if __name__ == "__main__":
    debug_populate()

