from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url="https://paisa.example.com")
        page = context.new_page()
        
        print("Navigating to login page...")
        page.goto("/login")
        
        print("Filling credentials...")
        page.fill("id=email", "test_user_a@example.com")
        page.fill("id=password", "Password123!")
        
        # Monitor network requests
        def handle_response(response):
            if "login" in response.url or "auth" in response.url:
                print(f"Auth Response: {response.status} {response.url}")
                try:
                    print(f"Body: {response.text()[:200]}")
                except:
                    pass
        
        page.on("response", handle_response)
        
        print("Clicking Sign In...")
        page.click("button[type='submit']:has-text('Sign In')")
        
        page.wait_for_timeout(5000)
        print(f"Final URL: {page.url}")
        
        error = page.query_selector("text=Invalid email or password")
        if error:
            print(f"Error Message: {error.inner_text()}")
        
        page.screenshot(path="login_debug.png")
        browser.close()

if __name__ == "__main__":
    run()

