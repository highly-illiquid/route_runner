import os
import json
from google import genai
from google.genai import types
from src.models import InvoiceBatch

class AIExtractor:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_KEY")
        self.model_name = "gemini-2.5-flash" 
        if not self.api_key:
            raise ValueError("GEMINI_KEY environment variable must be set.")
        self.client = genai.Client(api_key=self.api_key)

    def extract_invoice_data(self, file_bytes: bytes, mime_type: str = "application/pdf") -> InvoiceBatch:
        """
        Sends file bytes to Gemini 2.5 Flash and returns a validated InvoiceBatch object.
        Supports PDF and Images.
        """
        print(f"  (AI) Sending to model: {self.model_name} ({mime_type})...")
        
        prompt = """
        You are an expert data extraction agent. Your task is to process a document containing Bill of Ladings (BOLs).

        **CRITICAL FILTERING INSTRUCTIONS:**
        - The document may contain NOISE, such as Fax Cover Sheets, Blank Pages, or irrelevant instruction pages.
        - **IGNORE** these pages completely.
        - ONLY extract data from valid Bill of Lading pages.
        - If a page is a cover sheet, skip it.

        **DATA EXTRACTION INSTRUCTIONS:**
        - Extract ALL data fields for each valid BOL into a JSON list.
        - **TABLE ACCURACY IS PARAMOUNT.** The "SHIPMENT_DETAILS" table may contain **50+ line items**. You must capture **EVERY SINGLE ROW**. Do not summarize, do not truncate.
        - **REFERENCES:** Pay extreme attention to the "SHIPPER'S_REFERENCE" and "CONSIGNEE'S_PO" columns. 
          - These often contain MULTIPLE values per row. 
          - Capture ALL values as lists. 
          - Ensure the values line up correctly with their respective items.

        **FIELDS TO EXTRACT:**
        Match this exact JSON structure:
        1. "SHIPPERS_BOL#" (The main identifier)
        2. "CONSIGNEE_INFO" (Name, Address, Phone)
        3. "SHIPMENT_DETAILS" (Description, Pieces, Weight, Shipper's Refs, Consignee POs, Packing List)
        4. "CONSIGNEE_RECEIPT_INFO" (Who signed, date, time)
        5. "SPECIAL_DELIVERY_INSTRUCTIONS" (Notes, Gate codes, Call instructions)
        6. "BILLABLE_ACCESSORIALS" (Lift Gate, Inside Delivery, etc.)
        
        If a field is empty, return null.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        parts=[
                            types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                            types.Part.from_text(text=prompt)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=InvoiceBatch
                )
            )
            
            if not response.parsed:
                 raise ValueError("Gemini returned no parsed data.")
                 
            return response.parsed

        except Exception as e:
            print(f"AI Extraction Error: {e}")
            raise