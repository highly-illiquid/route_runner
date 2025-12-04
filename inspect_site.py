from playwright.sync_api import sync_playwright

def inspect_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating...")
        page.goto("https://www.infoconb2bcloud.com/Default.asp")
        
        print("Page Title:", page.title())
        
        # Dump form HTML to see inputs
        # Looking for inputs with type text/password
        inputs = page.locator("input").all()
        print(f"Found {len(inputs)} inputs.")
        
        for i in inputs:
            outer = i.evaluate("el => el.outerHTML")
            print(f"Input: {outer}")

        # Look for buttons
        buttons = page.locator("button, input[type='submit']").all()
        for b in buttons:
             outer = b.evaluate("el => el.outerHTML")
             print(f"Button: {outer}")
             
        browser.close()

if __name__ == "__main__":
    inspect_login()
