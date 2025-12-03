# Tech Context

## Technologies Used
*   **Language:** Python 3.10+
*   **Runtime:** GitHub Actions (ubuntu-latest runner)
*   **AI Model:** Google Gemini 2.5 Flash (via `google-genai` SDK)
*   **Browser Automation:** Playwright (Chromium)
*   **Data Validation:** Pydantic
*   **Email Protocols:** IMAP (fetching), SMTP (sending)

## Development Setup
*   **Local Environment:**
    *   Python 3.10+ installed.
    *   `pip install -r requirements.txt` (to be created).
    *   `playwright install chromium`
    *   Environment variables set in `.env` (for local testing): `EMAIL_USER`, `EMAIL_PASS`, `GEMINI_KEY`, `NOTIFY_EMAIL`.
*   **CI/CD:**
    *   GitHub Actions workflow defined in `.github/workflows/invoice-bot.yml` (derived from `github_scheduler.yml`).
    *   Secrets configured in GitHub Repository Settings.

## Technical Constraints
*   **Infocon Portal:**
    *   No API available.
    *   Subject to potential downtime or UI changes.
    *   Requires valid login session.
*   **GitHub Actions:**
    *   Execution time limits (though 15 mins is sufficient for typical batches).
    *   Ephemeral file system (files downloaded are lost after run).
*   **Email:**
    *   Reliance on Gmail IMAP availability.
    *   Attachment size limits (standard email limits apply).

## Dependencies
*   `google-genai`
*   `playwright`
*   `pydantic`
*   `pandas` (mentioned in example, TBD if strictly needed for final logic)
