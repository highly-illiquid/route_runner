import os
import json
from google import genai
from google.genai import types
from src.models import BillOfLading

class AIExtractor:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_KEY environment variable must be set.")
        self.client = genai.Client(api_key=self.api_key)

    def extract_invoice_data(self, file_bytes: bytes) -> BillOfLading:
        """
        Sends PDF bytes to Gemini 2.5 Flash and returns a validated BillOfLading object.
        """
        prompt = "Extract the Bill of Lading number, date, shipper name, and all line items (description, pieces, weight) from this invoice."
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
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
                    response_schema=BillOfLading
                )
            )
            
            # verify we got a valid response
            if not response.parsed:
                 raise ValueError("Gemini returned no parsed data.")
                 
            return response.parsed

        except Exception as e:
            print(f"AI Extraction Error: {e}")
            raise
