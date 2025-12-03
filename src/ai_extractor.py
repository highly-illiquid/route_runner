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

    def extract_invoice_data(self, file_bytes: bytes) -> InvoiceBatch:
        """
        Sends PDF bytes to Gemini 2.5 Flash and returns a validated InvoiceBatch object.
        """
        print(f"  (AI) Sending to model: {self.model_name}...")
        
        prompt = """
        Analyze this document containing one or more Bill of Ladings (BOLs).
        Extract ALL data fields for each BOL into a JSON list, matching this exact structure.
        
        Pay close attention to:
        1. "SHIPPERS_BOL#" (The main identifier)
        2. "CONSIGNEE_INFO" (Name, Address, Phone)
        3. "SHIPMENT_DETAILS" (Can have multiple references/POs per line item. Ensure you capture ALL Shipper's Refs and Consignee POs).
        4. "CONSIGNEE_RECEIPT_INFO" (Who signed for it, date, time).
        5. "SPECIAL_DELIVERY_INSTRUCTIONS" (Look for notes like "Call before delivery" etc).
        6. "BILLABLE_ACCESSORIALS" (e.g., "LIFT GATE", "INSIDE DELIVERY").
        
        If a field is empty in the document, return null.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        parts=[
                            types.Part.from_bytes(data=file_bytes, mime_type="application/pdf"),
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
