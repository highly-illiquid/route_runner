# Invisible Invoice Bot

A serverless automation tool that fetches PDF invoices from email, extracts data using Google Gemini AI, and automatically enters it into the Infocon WebEDI Portal using a headless browser.

## 🚀 Overview

*   **Goal:** Automate invoice processing for ~1,000 invoices/month.
*   **Stack:** Python, Playwright, Google Gemini 2.5 Flash.
*   **Experience:** Drag-and-drop. Save a PDF to `invoices/input` -> Data appears in the portal -> File moves to `invoices/archive`.

## 🛠️ Architecture

1.  **Trigger:** Script is run manually or via cron.
2.  **Scan:** Checks `invoices/input` for PDF files.
3.  **Extract:** Sends PDF attachments to **Gemini 2.5 Flash** to extract structured data (BOL #, Shipper, Line Items).
4.  **Upload:** Launches a headless **Playwright** browser to log in to the Infocon WebEDI portal and input the data.
5.  **Archive:** Moves processed files to `invoices/archive/[Date]/[Status]/`.
6.  **Report:** Emails a summary report of successes and errors to the developer.

## ⚙️ Setup & Configuration

### Prerequisites

*   Python 3.10+
*   A Google Cloud Project with Gemini API Access.
*   A Gmail account (for sending reports).
*   Infocon WebEDI Portal credentials.

### Environment Variables

The application requires the following environment variables.

| Variable | Description |
| :--- | :--- |
| `GEMINI_KEY` | **Required.** Google Gemini API Key. |
| `EMAIL_USER` | **Optional.** Gmail address for sending reports. |
| `EMAIL_PASS` | **Optional.** Gmail App Password. |
| `NOTIFY_EMAIL` | **Optional.** Email address to receive the summary report. |
| `PORTAL_USER` | (Optional/Future) Infocon Portal Username. |
| `PORTAL_PASS` | (Optional/Future) Infocon Portal Password. |

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/highly-illiquid/route_runner.git
    cd route_runner
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

3.  **Prepare Directories:**
    ```bash
    mkdir -p invoices/input
    ```

4.  **Run the bot:**
    ```bash
    # Place PDFs in invoices/input/ first!
    export GEMINI_KEY="your_key"
    
    python main.py
    ```

## 📂 Project Structure

```
route_runner/
├── .github/workflows/   # GitHub Actions CI/CD configuration
├── memory_bank/         # Project documentation & context
├── src/
│   ├── ai_extractor.py  # Gemini API integration
│   ├── email_client.py  # IMAP fetch & SMTP send logic
│   ├── models.py        # Pydantic data models
│   └── portal_bot.py    # Playwright browser automation
├── main.py              # Entry point / Orchestrator
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🤖 Automation

The project is configured to run automatically via GitHub Actions. See `.github/workflows/invoice-bot.yml` for the schedule configuration.

## 📄 License

[MIT](LICENSE)
