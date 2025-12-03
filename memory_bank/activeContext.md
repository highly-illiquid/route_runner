# Active Context

## Current Work Focus
We are currently in the **Initialization Phase**. The project structure is being set up, and the core logic is being ported from the example `auto_invoice_bot.py` script into a modular, production-ready structure as defined in the `project_brief.md`.

## Recent Changes
*   **Architecture Overhaul:** Implemented "Quarantine Workflow" (`Input -> Staging -> Archive/Quarantine`).
    *   Decoupled extraction from upload for safety.
    *   Added `invoices/staging` and `invoices/quarantine`.
    *   Implemented logic to retry staged files automatically.
*   **Workflow Refactor:** Switched from Email/IMAP -> Local File System.
*   **Feature Removal:** Removed Email Module.
*   **Data Model:** Comprehensive JSON schema support.

## Next Steps
1.  **Browser Automation:** Replace the mock `PortalBot` with real Playwright selectors.
    *   **Needs:** Login URL and HTML form details.
2.  **User Testing:** Verify the "Quarantine" recovery flow (e.g., verify that moving a fixed JSON from Quarantine to Staging actually works).

## Active Decisions
*   **Refactoring Strategy:** We are moving immediately from the single-file prototype to the modular structure to ensure maintainability from the start.
*   **Testing:** We will need to implement a way to mock the email and browser parts for local testing without hitting production systems, although the immediate focus is on structure.
