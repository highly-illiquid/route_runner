import asyncio
import imaplib
import email
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from google import genai
from google.genai import types
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field
from typing import List

# --- SECRETS (From GitHub Actions) ---
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL") # Where to send the summary report

# --- DATA MODELS ---
class LineItem(BaseModel):
    description: str = Field(..., description="Description of goods")
    pieces: int = Field(..., description="Number of pieces")
    weight: str = Field(..., description="Weight with units")

class BillOfLading(BaseModel):
    bol_number: str = Field(..., description="Shipper's BOL #")
    date: str = Field(..., description="Date of the document")
    shipper_name: str = Field(..., description="Name of the shipping company")
    items: List[LineItem] = Field(..., description="List of items in the table")

# --- HELPER: SEND SUMMARY EMAIL ---
def send_summary(processed_count, errors):
    if processed_count == 0 and not errors:
        return # Don't spam if nothing happened

    subject = f"Invoice Bot Report: {processed_count} Processed"
    body = f"Run complete at {datetime.now()}.\n\nProcessed: {processed_count} invoices.\n\n"
    
    if errors:
        subject += " [HAS ERRORS]"
        body += "Errors encountered:\n" + "\n".join(errors)
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = NOTIFY_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("Summary email sent.")
    except Exception as e:
        print(f"Failed to send summary email: {e}")

# --- 1. EMAIL FETCHER ---
def get_unread_invoices_data():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Search for unread emails with "Invoice" in subject
    status, messages = mail.search(None, '(UNSEEN SUBJECT "Invoice")')
    
    file_data_list = [] # List of (filename, bytes)

    for num in messages[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                        continue
                    
                    filename = part.get_filename()
                    if filename and filename.lower().endswith(".pdf"):
                        file_data = part.get_payload(decode=True)
                        file_data_list.append((filename, file_data))
                        print(f"Found: {filename}")
        
        # Mark as read so we don't process it again next hour
        mail.store(num, '+FLAGS', '\\Seen')

    mail.close()
    mail.logout()
    return file_data_list

# --- 2. GEMINI EXTRACTION ---
def extract_data(file_bytes):
    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(
                parts=[
                    types.Part.from_bytes(data=file_bytes, mime_type="application/pdf"),
                    types.Part.from_text(text="Extract BOL number, date, shipper, and line items.")
                ]
            )
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BillOfLading
        )
    )
    return response.parsed

# --- 3. BROWSER AUTOMATION ---
async def upload_invoice(data):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # --- REPLACE WITH REAL PORTAL LOGIC ---
            print(f"Simulating upload for BOL {data.bol_number}...")
            # await page.goto("https://portal.example.com")
            # await page.fill("#username", "admin")
            # await page.click("#login")
            # await page.fill("#bol", data.bol_number)
            # await page.click("#submit")
            # --------------------------------------
            return True
        except Exception as e:
            raise e
        finally:
            await browser.close()

# --- MAIN ORCHESTRATOR ---
async def main():
    print(f"--- Bot Starting: {datetime.now()} ---")
    
    # 1. Get Files (In Memory, no saving to disk needed for Cloud)
    try:
        invoices = get_unread_invoices_data()
    except Exception as e:
        print(f"Email fetch failed: {e}")
        return

    success_count = 0
    errors = []

    # 2. Process
    for filename, file_bytes in invoices:
        try:
            print(f"Extracting {filename}...")
            data = extract_data(file_bytes)
            
            print(f"Uploading {data.bol_number}...")
            await upload_invoice(data)
            
            success_count += 1
        except Exception as e:
            error_msg = f"Failed {filename}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)

    # 3. Report
    send_summary(success_count, errors)
    print("--- Run Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
