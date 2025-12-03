# Product Context

## Why This Project Exists
This project aims to eliminate the manual data entry burden for a client who processes approximately 1,000 invoices per month. The current manual process is time-consuming and prone to human error. By automating the extraction of data from emailed PDF invoices and the entry of that data into the Infocon WebEDI Portal, we can significantly improve efficiency and accuracy.

## Problem Solved
The Infocon WebEDI Portal is a managed service that lacks a public API, forcing users to manually input data via a web interface. This project bridges the gap between the client's incoming email invoices (unstructured/semi-structured data) and the portal (structured web forms) without requiring manual intervention.

## How It Works
The system operates as a local batch processing tool.
1.  **Input:** The user saves PDF invoices into a local directory (`invoices/input`).
2.  **Processing:** The script runs (manually or via cron):
    *   Scans the input directory for PDFs.
    *   Extracts structured data (BOL #, Date, Shipper, Line Items) using Gemini 2.5 Flash.
    *   Automate the web browser (Playwright) to log in to Infocon and enter the data.
3.  **Archiving:**
    *   **Success:** Files are moved to `invoices/archive/YYYY-MM-DD/processed/`.
    *   **Failure:** Files are moved to `invoices/archive/YYYY-MM-DD/failed/`.
4.  **Reporting:** A summary email is sent to the developer with a count of processed invoices and any errors encountered.

## User Experience Goals
*   **Local Control:** The user manages the input files directly on their file system.
*   **Clean Organization:** The system automatically organizes processed files by date and status, keeping the input folder clean.
*   **Reliability:** The system handles errors gracefully and notifies the developer.
*   **Accuracy:** High-fidelity data extraction and entry.
