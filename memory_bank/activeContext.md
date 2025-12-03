# Active Context

## Current Work Focus
We are currently in the **Initialization Phase**. The project structure is being set up, and the core logic is being ported from the example `auto_invoice_bot.py` script into a modular, production-ready structure as defined in the `project_brief.md`.

## Recent Changes
*   **Modularization Completed:**
    *   `src/models.py`, `src/email_client.py`, `src/ai_extractor.py`, `src/portal_bot.py`, `main.py`.
*   **CI/CD Configured:** Created `.github/workflows/invoice-bot.yml`.
*   **Cleanup:** Removed `auto_invoice_bot.py` and `github_scheduler.yml`.
*   **Documentation:** Added `README.md`.
*   **Git:** Successfully pushed all changes to `origin/master` via HTTPS.

## Next Steps
1.  **User Verification:** User to verify the repository on GitHub.
2.  **Local Testing:** Setup `.env` variables to run the bot locally if desired.

## Active Decisions
*   **Refactoring Strategy:** We are moving immediately from the single-file prototype to the modular structure to ensure maintainability from the start.
*   **Testing:** We will need to implement a way to mock the email and browser parts for local testing without hitting production systems, although the immediate focus is on structure.
