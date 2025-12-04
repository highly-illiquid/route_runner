from playwright.async_api import async_playwright, Page
from src.models import BillOfLading
import asyncio
import os

class PortalBot:
    def __init__(self):
        self.portal_user = os.environ.get("PORTAL_USER")
        self.portal_pass = os.environ.get("PORTAL_PASS")
        
        if not self.portal_user or not self.portal_pass:
            print("Warning: PORTAL_USER or PORTAL_PASS missing. Browser automation will fail login.")

    async def upload_invoice(self, data: BillOfLading):
        """
        Launches a headless browser, logs in, and enters the invoice data.
        """
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await self.login(page)
                
                # Uncomment these when we are ready to proceed
                # await self.navigate_to_create(page)
                # await self.fill_form(page, data)
                # await self.submit(page)
                
                print(f"Successfully uploaded BOL: {data.shippers_bol_number}")
                
            except Exception as e:
                print(f"Browser Automation Error for {data.shippers_bol_number}: {e}")
                # Save error screenshot
                screenshot_path = f"error_{data.shippers_bol_number}.png"
                await page.screenshot(path=screenshot_path)
                print(f"Saved screenshot to {screenshot_path}")
                raise e # CRITICAL: Re-raise exception so main.py knows to Quarantine
            finally:
                await browser.close()

    async def login(self, page: Page):
        print("  Logging in to Infocon...")
        await page.goto("https://www.infoconb2bcloud.com/Default.asp")
        
        # Wait for inputs
        await page.wait_for_selector("#userId")
        
        # Fill Credentials
        await page.fill("#userId", self.portal_user)
        await page.fill("#password", self.portal_pass)
        
        # Click Login
        await page.click("input[value='Login']")
        
        # Wait for navigation or 2FA prompt
        print("  Waiting for response...")
        await asyncio.sleep(5) 
        
        # VALIDATION LOGIC
        current_url = page.url
        if "Default.asp" in current_url:
            # Check for specific failure indicators
            content = await page.content()
            if "verificationCode" in content or "Send Verification Code" in content:
                 raise Exception("Login Failed: 2FA/Verification Code required.")
            else:
                 raise Exception(f"Login Failed: URL did not change. Still on {current_url}")
        
        print(f"  Login successful. URL: {current_url}")

    async def navigate_to_create(self, page: Page):
        print("  Navigating to 'Create Invoice'...")
        # await page.click("text=New Invoice")
        await asyncio.sleep(0.5)

    async def fill_form(self, page: Page, data: BillOfLading):
        print(f"  Filling form for BOL {data.shippers_bol_number}...")

    async def submit(self, page: Page):
        print("  Submitting form...")
        # await page.click("#save_button")
        await asyncio.sleep(1)