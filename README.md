# Invisible Invoice Bot

A serverless automation tool that fetches PDF invoices from email, extracts data using Google Gemini AI, and automatically enters it into the Infocon WebEDI Portal using a headless browser.

## 🚀 Overview

*   **Goal:** Automate invoice processing for ~1,000 invoices/month.
*   **Stack:** Python, Playwright, Google Gemini 2.5 Flash, GitHub Actions.
*   **Experience:** "Invisible" workflow. Email an invoice -> Data appears in the portal.

## 🛠️ Architecture

1.  **Trigger:** GitHub Action runs hourly (`0 * * * *`).
2.  **Fetch:** Connects to Gmail via IMAP to find unread emails with "Invoice" in the subject.
3.  **Extract:** Sends PDF attachments to **Gemini 2.5 Flash** to extract structured data (BOL #, Shipper, Line Items).
4.  **Upload:** Launches a headless **Playwright** browser to log in to the Infocon WebEDI portal and input the data.
5.  **Report:** Emails a summary report of successes and errors to the developer.

## ⚙️ Setup & Configuration

### Prerequisites

*   Python 3.10+
*   A Google Cloud Project with Gemini API Access.
*   A Gmail account (with App Password enabled for IMAP/SMTP).
*   Infocon WebEDI Portal credentials.

### Environment Variables

The application requires the following environment variables. For local development, you can set these in your shell or use a `.env` file manager. For GitHub Actions, add them to **Settings > Secrets and variables > Actions**.

| Variable | Description |
| :--- | :--- |
| `EMAIL_USER` | Gmail address for fetching/sending. |
| `EMAIL_PASS` | Gmail App Password (not your login password). |
| `GEMINI_KEY` | Google Gemini API Key. |
| `NOTIFY_EMAIL` | Email address to receive the summary report. |
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

3.  **Run the bot:**
    ```bash
    # Ensure env vars are set
    export EMAIL_USER="your_email@gmail.com"
    export EMAIL_PASS="your_app_password"
    export GEMINI_KEY="your_gemini_key"
    export NOTIFY_EMAIL="your_email@gmail.com"
    
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
