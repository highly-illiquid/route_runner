# Project: Invisible Invoice Bot (GitHub Actions)

## 1. Executive Summary
*   **Goal:** Automate invoice processing for a single client (approx. 1,000 invoices/month) into the Infocon WebEDI Portal.
*   **Client Experience:** "Invisible." They email an invoice; data automagically appears in their Infocon portal.
*   **Developer Experience:** Neovim + Gemini CLI. Code is modular, typed, and robust.
*   **Constraint:** Infocon is a managed service with NO public API. Automation must be performed via Headless Browser (Playwright) simulating a human user on the WebEDI interface.

## 2. Architecture & Stack
*   **Infrastructure:** GitHub Actions (Serverless Cron Job).
*   **Language:** Python 3.10+.
*   **Core Libraries:**
    *   `google-genai`: AI Extraction (Model: gemini-2.5-flash).
    *   `playwright`: Headless Browser Automation (Infocon WebEDI Interaction).
    *   `imaplib` / `email`: Fetching PDFs from Gmail.
    *   `pydantic`: Robust data validation and schema definition.
*   **Secrets Management:** GitHub Repository Secrets (Infocon Credentials, API Keys).

## 3. Workflow Logic (The "Automagic" Loop)
1.  **Trigger:** GitHub Action runs hourly (cron: `'0 * * * *'`).
2.  **Fetch:** Script connects to `processing@agency.com` via IMAP and downloads unread PDF attachments matching "Subject: Invoice".
3.  **Extract:** PDFs are sent to Gemini 2.5 Flash API.
    *   **Input:** PDF Bytes.
    *   **Output:** JSON (BOL #, Date, Shipper, Line Items).
4.  **Upload (The Infocon Bot):** Playwright launches Headless Chromium.
    *   **Login:** Navigates to Infocon WebEDI URL, enters User/Pass.
    *   **Navigation:** Clicks through menus to "Create New Invoice/BOL".
    *   **Data Entry:** Types extracted JSON data into HTML form fields.
    *   **Submission:** Clicks "Save/Submit" and verifies the "Success" toast/message.
5.  **Report:** Script compiles a success/error log and emails a summary to the developer (You).

## 4. Implementation Plan (Files)
### A. `src/models.py` (Data Structures)
Define Pydantic models to ensure Gemini returns strict JSON.
*   `LineItem`: description (str), pieces (int), weight (str).
*   `BillOfLading`: bol_number, date, shipper, items (List[LineItem]).

### B. `src/email_client.py` (Input/Output)
*   `get_unread_invoices()`: Connects to IMAP, filters by subject, downloads PDF bytes, marks as read.
*   `send_summary_email()`: Uses SMTP to email a run report.

### C. `src/ai_extractor.py` (The Brain)
*   `extract_invoice_data(pdf_bytes) -> BillOfLading`: Calls Gemini 2.5 Flash with the PDF and the Pydantic schema.

### D. `src/portal_bot.py` (The Hands)
*   `class InfoconBot`:
    *   `login()`
    *   `navigate_to_create()`
    *   `fill_form(data: BillOfLading)`
    *   `submit()`

### E. `main.py` (The Conductor)
Orchestrates the flow: Fetch -> Extract -> Upload -> Report.