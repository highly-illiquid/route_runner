# System Patterns

## System Architecture
The system is designed as a **Local Batch Processor**. It follows a linear pipeline architecture:
`Input (Local Dir) -> Processing (Extraction & Transformation) -> Output (Web Automation) -> Archiving -> Reporting`

### Key Components
1.  **File Manager (`src/file_manager.py`):** Handles scanning input directories, reading PDF bytes, and moving files to archive folders based on processing status.
2.  **Email Notifier (`src/email_client.py`):** Handles SMTP connections to send summary reports (Success/Error logs).
3.  **AI Extractor (`src/ai_extractor.py`):** leverages Google's Gemini 2.5 Flash model via `google-genai` library to convert unstructured PDF data into structured JSON based on Pydantic models.
4.  **Data Models (`src/models.py`):** Defines the schema for `BillOfLading` and `LineItem` using Pydantic, ensuring type safety and validation.
5.  **Portal Bot (`src/portal_bot.py`):** Uses Playwright for headless browser automation to interact with the Infocon WebEDI interface.
6.  **Orchestrator (`main.py`):** Coordinates the workflow, error handling, and logging.

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
