# Active Context

## Current Work Focus
We are currently in the **Initialization Phase**. The project structure is being set up, and the core logic is being ported from the example `auto_invoice_bot.py` script into a modular, production-ready structure as defined in the `project_brief.md`.

## Recent Changes
*   Created `memory_bank/` directory and initialized all context files.
*   Created project directories: `src/`, `.github/workflows/`.
*   Created `requirements.txt`.

## Next Steps
1.  **Modularization:** Refactor the monolithic `auto_invoice_bot.py` into the planned modules:
    *   `src/models.py`
    *   `src/email_client.py`
    *   `src/ai_extractor.py`
    *   `src/portal_bot.py`
    *   `main.py`
2.  **GitHub Workflow:** Adapt `github_scheduler.yml` to the new structure and save as `.github/workflows/invoice-bot.yml`.
3.  **Clean Up:** Remove the temporary example files (`auto_invoice_bot.py`, `github_scheduler.yml`) once refactoring is verified.

## Active Decisions
*   **Refactoring Strategy:** We are moving immediately from the single-file prototype to the modular structure to ensure maintainability from the start.
*   **Testing:** We will need to implement a way to mock the email and browser parts for local testing without hitting production systems, although the immediate focus is on structure.
