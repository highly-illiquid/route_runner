# Active Context

## Current Work Focus
We are currently in the **Initialization Phase**. The project structure is being set up, and the core logic is being ported from the example `auto_invoice_bot.py` script into a modular, production-ready structure as defined in the `project_brief.md`.

## Recent Changes
*   **Architecture Overhaul:** Implemented "Quarantine Workflow" (`Input -> Staging -> Archive/Quarantine`).
*   **2FA Automation:** Implemented automated email verification loop in `src/portal_bot.py` using IMAP.
    *   Logic: Poll `[Gmail]/All Mail` for `TEXT` matching Subject, extract code via Regex.
*   **Issue:** `test_2fa_logic.py` successfully finds the 2FA email using this logic. However, `main.py` (using the same logic) fails to find the email during live execution, even when the email is present and unread.
*   **Feature Removal:** Removed `src/email_client.py` (SMTP Reporting) due to auth issues.

## Next Steps
1.  **Debug 2FA in Main:** Investigate why `main.py` execution context differs from `test_2fa_logic.py` (Env vars? Library version? Async conflict?).
2.  **Browser Automation:** Once login passes, implement `navigate_to_create` and `fill_form` using real selectors.
3.  **User Testing:** Verify the "Quarantine" recovery flow.

## Critical Testing Rule
ALWAYS verify 2FA logic using `test_2fa_logic.py` before running `main.py`. The Infocon portal has strict rate limits.

## Active Decisions
*   **Refactoring Strategy:** We are moving immediately from the single-file prototype to the modular structure to ensure maintainability from the start.
*   **Testing:** We will need to implement a way to mock the email and browser parts for local testing without hitting production systems, although the immediate focus is on structure.
*   **Critical Testing Rule:** ALWAYS verify 2FA logic using `test_2fa_logic.py` before running `main.py`. The Infocon portal has strict rate limits, and failed 2FA attempts can lead to permanent lockout. Never spam `main.py` for debugging auth logic.
