# Progress

## Status
*   **Project Status:** Initialization / Refactoring
*   **Build Status:** Not yet configured (Workflow file exists as example but needs moving).
*   **Test Coverage:** 0%

## What Works
*   **Concept:** The logic in `auto_invoice_bot.py` provides a working proof-of-concept for the individual steps (Email -> AI -> Browser).
*   **Documentation:** Memory Bank is initialized and aligned with the project goals.

## What's Left to Build
*   [x] **Project Scaffolding:** Create folders and files.
*   [x] **Dependencies:** `requirements.txt`.
*   [x] **Module: Models:** `src/models.py` (Comprehensive).
*   [x] **Module: AI:** `src/ai_extractor.py` (Gemini 2.5 Flash).
*   [x] **Module: File Manager:** `src/file_manager.py`.
*   [x] **Main Entry Point:** `main.py`.
*   [x] **Verification:** Local run success with correct JSON output.
*   [ ] **Module: Bot:** `src/portal_bot.py`
    *   [x] Login Selectors.
    *   [~] **2FA Automation:** Logic works in `test_2fa_logic.py` but fails in `main.py`. Blocked by IMAP visibility issue.
    *   [ ] Form Filling (Requires Login success).
*   [x] **Module: Email:** Removed due to auth issues.

## Known Issues
*   **SMTP:** Removed reporting feature.
*   **IMAP 2FA:** Bot fails to find unread 2FA emails in `[Gmail]/All Mail` during live run, despite `test_2fa_logic.py` succeeding with identical code. Potential async/environment issue.

## Known Issues
*   None currently (pre-implementation).
