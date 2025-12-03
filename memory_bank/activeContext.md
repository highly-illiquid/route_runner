# Active Context

## Current Work Focus
We are currently in the **Initialization Phase**. The project structure is being set up, and the core logic is being ported from the example `auto_invoice_bot.py` script into a modular, production-ready structure as defined in the `project_brief.md`.

## Recent Changes
*   **Workflow Refactor:** Switched from Email/IMAP -> Local File System (`invoices/input` -> `invoices/archive`).
*   **Data Model Upgrade:** Updated `src/models.py` to capture comprehensive BOL details.
*   **Logging:** Added JSON file logging alongside archived PDFs.
*   **Feature Removal:** Removed `src/email_client.py` (SMTP Reporting) due to persistent `535 BadCredentials` errors despite valid credentials.

## Next Steps
1.  **Browser Automation:** Replace the mock `PortalBot` with real Playwright selectors.
    *   **Needs:** Login URL and HTML form details.
2.  **Refinement:** Test with more complex PDFs to ensure AI robustness.

## Active Decisions
*   **Refactoring Strategy:** We are moving immediately from the single-file prototype to the modular structure to ensure maintainability from the start.
*   **Testing:** We will need to implement a way to mock the email and browser parts for local testing without hitting production systems, although the immediate focus is on structure.
