from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url="https://paisa.example.com")
        page = context.new_page()
        
        page.goto("/login")
        print("Login Page Source:")
        # print(page.content()) # Too much output
        
        # Try to register
        page.click("button:has-text('Register')")
        page.fill("id=email", "newtestuser@example.com")
        page.fill("id=password", "Password123!")
        page.keyboard.press("Enter")
        
        try:
            page.wait_for_url("**/dashboard", timeout=15000)
            print("Logged in!")
            
            # Click Record Trade
            page.click("button:has-text('Record New Trade')")
            page.wait_for_selector("form", timeout=5000)
            
            # Save HTML of the form
            form_html = page.eval_on_selector("form", "el => el.outerHTML")
            with open("trade_form.html", "w") as f:
                f.write(form_html)
            print("Trade form HTML saved to trade_form.html")
            
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="error.png")
            with open("error_page.html", "w") as f:
                f.write(page.content())
        
        browser.close()

if __name__ == "__main__":
    run()

