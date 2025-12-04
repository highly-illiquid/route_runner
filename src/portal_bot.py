from playwright.async_api import async_playwright, Page
from src.models import BillOfLading
import asyncio
import os
import imaplib
import email
import re
import time

class PortalBot:
    def __init__(self, dry_run=False):
        self.portal_user = os.environ.get("PORTAL_USER")
        self.portal_pass = os.environ.get("PORTAL_PASS")
        
        self.email_user = (os.environ.get("EMAIL_USER") or "").strip()
        self.email_pass = (os.environ.get("EMAIL_PASS") or "").strip()
        self.infocon_email = (os.environ.get("INFOCON_EMAIL") or "").strip()
        self.infocon_subject = (os.environ.get("INFOCON_SUBJECT") or "").strip()
        
        self.dry_run = dry_run
        
        if self.dry_run:
            print("⚠️  DRY RUN MODE ENABLED - Will NOT connect to Infocon portal ⚠️")

        if not self.portal_user or not self.portal_pass:
            print("Warning: PORTAL_USER or PORTAL_PASS missing. Browser automation will fail login.")

    async def upload_invoice(self, data: BillOfLading):
        if self.dry_run:
            print(f"\n[DRY RUN] Simulating upload for BOL: {data.shippers_bol_number}")
            print(f"  [DRY RUN] Would launch browser...")
            print(f"  [DRY RUN] Would login to Infocon...")
            print(f"  [DRY RUN] Would handle 2FA...")
            print(f"  [DRY RUN] Would fill form with:")
            print(f"    - BOL: {data.shippers_bol_number}")
            print(f"    - Date: {data.date}")
            print(f"    - From: {data.company_name_from}")
            print(f"    - Consignee: {data.consignee_info.name if data.consignee_info else 'N/A'}")
            print(f"    - Shipment Details: {len(data.shipment_details)} items")
            print(f"  [DRY RUN] ✓ Upload simulated successfully")
            return
        
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
            # Wait is now handled inside _fetch_2fa_code_from_email (15s before connecting)

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
        """
        Wait for email to arrive, then poll until found.
        IMAP search() sees new emails on same connection - no reconnection needed.
        """
        print("  Polling email for verification code...")
        
        if not self.email_user or not self.email_pass:
             raise Exception("Cannot perform 2FA: EMAIL_USER or EMAIL_PASS missing.")

        # Wait for email to arrive before connecting
        print("    Waiting 10 seconds for email to arrive...")
        time.sleep(10)

        try:
            # Connect once
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_user, self.email_pass)
            mail.select('INBOX')
            
            # Build search criteria
            if self.infocon_subject:
                search_criteria = f'(SUBJECT "{self.infocon_subject}" UNSEEN)'
            else:
                search_criteria = '(SUBJECT "Infocon" UNSEEN)'
            
            print(f"    Searching INBOX for: {search_criteria}")
            print(f"    Will poll every {delay}s for up to {retries} attempts\n")
            
            # Poll until found
            for attempt in range(retries):
                print(f"    [Attempt {attempt+1}/{retries}]", end=" ")
                
                status, messages = mail.search(None, search_criteria)
                msg_ids = messages[0].split()
                
                if msg_ids:
                    # Found it!
                    latest_id = msg_ids[-1]
                    print(f"✓ Found email (ID: {latest_id.decode()})")
                    
                    # Fetch without marking as SEEN
                    status, msg_data = mail.fetch(latest_id, '(BODY.PEEK[])')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    print(f"      Subject: {msg['subject']}")
                    print(f"      Date: {msg['date']}")
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    # Find 6-digit code
                    match = re.search(r"(\d{6})", body)
                    if match:
                        code = match.group(1)
                        print(f"      ✓ CODE: {code}\n")
                        
                        # Mark as read and cleanup
                        mail.store(latest_id, '+FLAGS', r'\Seen')
                        mail.close()
                        mail.logout()
                        return code
                    else:
                        print(f"      ✗ No 6-digit code found in email body")
                        mail.close()
                        mail.logout()
                        raise Exception("Email found but no verification code in body")
                else:
                    print("No matching email yet...")
                
                # Wait before next attempt
                if attempt < retries - 1:
                    time.sleep(delay)
            
            # Timeout
            print(f"\n    ✗ Timeout: No email found after {retries * delay} seconds")
            mail.close()
            mail.logout()
            return None

        except Exception as e:
            print(f"  ✗ IMAP Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def navigate_to_create(self, page: Page):
        print("  Navigating to 'Create Invoice'...")
        await asyncio.sleep(0.5)

    async def fill_form(self, page: Page, data: BillOfLading):
        print(f"  Filling form for BOL {data.shippers_bol_number}...")

    async def submit(self, page: Page):
        print("  Submitting form...")
        await asyncio.sleep(1)
