# Product Context

## Why This Project Exists
This project aims to eliminate the manual data entry burden for a client who processes approximately 1,000 invoices per month. The current manual process is time-consuming and prone to human error. By automating the extraction of data from emailed PDF invoices and the entry of that data into the Infocon WebEDI Portal, we can significantly improve efficiency and accuracy.

## Problem Solved
The Infocon WebEDI Portal is a managed service that lacks a public API, forcing users to manually input data via a web interface. This project bridges the gap between the client's incoming email invoices (unstructured/semi-structured data) and the portal (structured web forms) without requiring manual intervention.

## How It Works
The system operates as an "invisible" background service.
1.  **Input:** The client or their vendors email PDF invoices to a designated address (`processing@agency.com`).
2.  **Processing:** A GitHub Action triggers hourly to:
    *   Fetch unread invoices via IMAP.
    *   Extract structured data (BOL #, Date, Shipper, Line Items) using Gemini 2.5 Flash.
    *   Automate the web browser (Playwright) to log in to Infocon and enter the data.
3.  **Output:** The data appears in the Infocon portal, ready for further processing or approval. A summary report is emailed to the developer.

## User Experience Goals
*   **"Invisible" Operation:** The client requires no new tools or interfaces. They simply continue their existing workflow of emailing invoices.
*   **Reliability:** The system handles errors gracefully (e.g., bad PDFs, portal downtime) and notifies the developer rather than failing silently.
*   **Accuracy:** High-fidelity data extraction and entry to minimize post-entry corrections.
