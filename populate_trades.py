import json
import os
import time
from playwright.sync_api import sync_playwright

# Configuration - update these with real credentials
EMAIL = os.environ.get("PAISA_TEST_EMAIL", "test_user_a@example.com")
PASSWORD = os.environ.get("PAISA_TEST_PASSWORD", "Password123!")
BASE_URL = "https://paisa.example.com"

def populate_trades():
    with open("trade_data.json", "r") as f:
        trades = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        print(f"Logging into {BASE_URL}...")
        page.goto("/login")
        
        # Using type instead of fill to trigger all events
        page.type("id=email", EMAIL, delay=50)
        page.type("id=password", PASSWORD, delay=50)
        
        submit_btn = page.locator("button[type='submit']:has-text('Sign In')")
        submit_btn.click()

        try:
            # Wait for the dashboard to load (signals login success)
            page.wait_for_selector(".text-2xl:has-text('Dashboard'), .text-3xl:has-text('Dashboard')", timeout=30000)
            print("Successfully logged in.")
            
            # Dismiss any guide modals via JS
            page.evaluate("""
                const closeBtn = Array.from(document.querySelectorAll('button')).find(b => 
                    b.querySelector('svg.lucide-x') || 
                    b.innerText.includes('Close') || 
                    b.getAttribute('aria-label') === 'Close guide'
                );
                if (closeBtn) closeBtn.click();
            """)
            
            # Extract token from localStorage
            token = page.evaluate("localStorage.getItem('session_token')")
            if not token:
                print("Error: Could not extract session token from localStorage.")
                browser.close()
                return

            print(f"Extracted session token. Proceeding to inject {len(trades)} trades via API...")

            for trade in trades:
                print(f"Injecting trade for {trade['ticker']} ({trade['date']})...")
                
                # Normalize trade data for the API
                # The backend expects: ticker, symbol, entry_price, quantity, action, trade_type, strategy_type, recorded_at
                payload = {
                    "ticker": trade['ticker'],
                    "symbol": trade.get('symbol', trade['ticker']),
                    "entry_price": trade['price'],
                    "quantity": trade['quantity'],
                    "action": trade.get('action', 'BUY'),
                    "trade_type": trade.get('trade_type', 'STOCK'),
                    "strategy_type": trade.get('strategy_type', 'Historical Import'),
                    "recorded_at": trade.get('date', time.strftime('%Y-%m-%d')) + "T10:00:00Z"
                }
                
                if 'expiry' in trade:
                    payload['expiry'] = trade['expiry']
                
                # Send the POST request directly via fetch in the browser context
                result = page.evaluate("""
                    async ({ url, token, payload }) => {
                        const response = await fetch(url + "/api/trades/save", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + token
                            },
                            body: JSON.stringify(payload)
                        });
                        return await response.json();
                    }
                """, {"url": BASE_URL, "token": token, "payload": payload})
                
                if result.get('status') == 'success':
                    print(f"  Successfully recorded {trade['ticker']}.")
                else:
                    print(f"  Failed to record {trade['ticker']}: {result.get('message', 'Unknown error')}")
                
                # Small delay to avoid overwhelming the server
                time.sleep(0.2)

            print("All trades processed.")
            
            # Navigate to dashboard to verify and take final screenshot
            page.goto("/dashboard")
            page.wait_for_timeout(2000)
            page.screenshot(path="final_dashboard_state.png", full_page=True)
            print("Final screenshot saved to final_dashboard_state.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="injection_failure_debug.png")
            with open("injection_failure_debug.html", "w", encoding="utf-8") as f:
                f.write(page.content())

        browser.close()

if __name__ == "__main__":
    populate_trades()

