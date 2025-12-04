from playwright.async_api import async_playwright, Page
from src.models import BillOfLading
import asyncio
import os
import imaplib
import email
import re
import time

class PortalBot:
    def __init__(self):
        self.portal_user = os.environ.get("PORTAL_USER")
        self.portal_pass = os.environ.get("PORTAL_PASS")
        
        self.email_user = (os.environ.get("EMAIL_USER") or "").strip()
        self.email_pass = (os.environ.get("EMAIL_PASS") or "").strip()
        self.infocon_email = (os.environ.get("INFOCON_EMAIL") or "").strip()
        self.infocon_subject = (os.environ.get("INFOCON_SUBJECT") or "").strip()

        if not self.portal_user or not self.portal_pass:
            print("Warning: PORTAL_USER or PORTAL_PASS missing. Browser automation will fail login.")

    async def upload_invoice(self, data: BillOfLading):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await self.login(page)
                print(f"Successfully uploaded BOL: {data.shippers_bol_number}")
                
            except Exception as e:
                print(f"Browser Automation Error for {data.shippers_bol_number}: {e}")
                screenshot_path = f"error_{data.shippers_bol_number}.png"
                await page.screenshot(path=screenshot_path)
                print(f"Saved screenshot to {screenshot_path}")
                raise e
            finally:
                await browser.close()

    async def login(self, page: Page):
        print("  Logging in to Infocon...")
        await page.goto("https://www.infoconb2bcloud.com/Default.asp")
        
        await page.wait_for_selector("#userId")
        await page.fill("#userId", self.portal_user)
        await page.fill("#password", self.portal_pass)
        await page.click("input[value='Login']")
        
        print("  Waiting for response...")
        await asyncio.sleep(5) 
        
        content = await page.content()
        if "verificationCode" in content or "Send Verification Code" in content:
            print("  2FA Screen Detected. Initiating automated verification...")
            await self._handle_2fa(page)
        elif "Default.asp" in page.url:
             raise Exception(f"Login Failed: URL did not change. Still on {page.url}")
        
        print(f"  Login successful. URL: {page.url}")

    async def _handle_2fa(self, page: Page):
        if await page.is_visible("input[value='Send Verification Code']"):
            print("  Clicking 'Send Verification Code'...")
            await page.click("input[value='Send Verification Code']")
            await asyncio.sleep(10)

        code = self._fetch_2fa_code_from_email()
        if not code:
            raise Exception("Failed to retrieve 2FA code from email.")

        print(f"  Entering Verification Code: {code}")
        
        await page.fill("#verificationCode", code)
        await page.click("input[value='Verify Code']")
        
        await asyncio.sleep(5)
        if "verificationCode" in await page.content():
             raise Exception("2FA Verification Failed (Invalid Code?).")

    def _fetch_2fa_code_from_email(self, retries=45, delay=10):
        print("  Polling email for verification code...")
        
        if not self.email_user or not self.email_pass:
             raise Exception("Cannot perform 2FA: EMAIL_USER or EMAIL_PASS missing.")

        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_user, self.email_pass)
            
            # FORCE ALL MAIL (No try/except)
            print("    [DEBUG] Selecting '[Gmail]/All Mail'...")
            mail.select('"[Gmail]/All Mail"')
            print("    [DEBUG] Selection Successful.")
            
            if self.infocon_subject:
                criteria = f'(TEXT "{self.infocon_subject}" UNSEEN)'
            else:
                criteria = '(TEXT "Infocon" UNSEEN)'
            
            print(f"    Using Criteria: {criteria}")
            
            for attempt in range(retries):
                print(f"    [Attempt {attempt+1}/{retries}] Searching...")
                status, messages = mail.search(None, criteria)
                msg_ids = messages[0].split()
                
                if msg_ids:
                    last_id = msg_ids[-1]
                    status, msg_data = mail.fetch(last_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    print(f"    [DEBUG] Found UNSEEN Email: {msg['subject']}")

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    match = re.search(r"code.*?(\d{6})", body, re.IGNORECASE | re.DOTALL)
                    if match:
                        code = match.group(1)
                        print(f"    FOUND CODE: {code}")
                        mail.store(last_id, '+FLAGS', '\Seen')
                        mail.close()
                        mail.logout()
                        return code
                    else:
                         print(f"    [DEBUG] Email found but Regex did not match code.")
                
                time.sleep(delay)
            
            mail.close()
            mail.logout()
            return None

        except Exception as e:
            print(f"  IMAP Error: {e}")
            return None

    async def navigate_to_create(self, page: Page):
        print("  Navigating to 'Create Invoice'...")
        await asyncio.sleep(0.5)

    async def fill_form(self, page: Page, data: BillOfLading):
        print(f"  Filling form for BOL {data.shippers_bol_number}...")

    async def submit(self, page: Page):
        print("  Submitting form...")
        await asyncio.sleep(1)
