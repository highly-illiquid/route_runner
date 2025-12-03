# System Patterns

## System Architecture
The system is designed as a **Resilient Local Batch Processor**. It follows a decoupled pipeline architecture to ensure safety and recoverability:

`Input -> [Extraction] -> Staging -> [Upload] -> Archive`

### Workflow Phases
1.  **Input Phase (`invoices/input`):**
    *   Raw PDFs/Images are picked up here.
    *   AI Extraction converts them to JSON.
    *   **Success:** JSON + Source File move to `Staging`.
    *   **Fail:** Source File moves to `Quarantine`.

2.  **Staging Phase (`invoices/staging`):**
    *   Holds files that have valid data but haven't been uploaded yet.
    *   Serves as a buffer/outbox. Allows for manual review if needed.

3.  **Upload Phase:**
    *   Reads JSON from `Staging`.
    *   Bot enters data into Infocon Portal.
    *   **Success:** JSON + Source File move to `Archive`.
    *   **Fail:** JSON + Source File move to `Quarantine`.

4.  **Quarantine Phase (`invoices/quarantine`):**
    *   Holding area for any item that requires human intervention.
    *   **Recovery:** User fixes the file (or JSON) and moves it back to `Input` or `Staging`.

### Key Components
1.  **File Manager (`src/file_manager.py`):** Handles complex state transitions between Input, Staging, Archive, and Quarantine. Manages file pairs (PDF+JSON).
2.  **AI Extractor (`src/ai_extractor.py`):** Gemini 2.5 Flash integration. Now robust against noise and coversheets.
3.  **Data Models (`src/models.py`):** Comprehensive Pydantic models matching the Portal's schema.
4.  **Portal Bot (`src/portal_bot.py`):** Playwright automation.
5.  **Orchestrator (`main.py`):** Runs the multi-phase loop (Retry Staging -> Process Input -> Upload New Staging).

## Technical Decisions
*   **GitHub Actions:** Chosen for zero-maintenance infrastructure and built-in secret management. The hourly cron schedule fits the batch processing nature of the task.
*   **Python 3.10+:** selected for its rich ecosystem for automation (`playwright`), AI integration (`google-genai`), and data handling (`pydantic`).
*   **Gemini 2.5 Flash:** Chosen for its cost-effectiveness and high performance in multimodal (text + image/PDF) extraction tasks.
*   **Playwright:** Selected over Selenium for its modern architecture, better handling of dynamic web content, and reliability in headless environments.
*   **Pydantic:** Used for rigorous data validation to ensure that only valid data is attempted to be entered into the portal.

## Critical Implementation Paths
1.  **Authentication:** Secure handling of Email credentials and Infocon Portal credentials via GitHub Secrets.
2.  **Selector Stability:** The `portal_bot.py` relies on CSS/XPath selectors. These must be robust to minor UI changes in the Infocon portal.
3.  **Error Handling:** The `main.py` loop must ensure that a failure in processing one invoice does not stop the batch. Failed invoices must be reported.
