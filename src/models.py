from typing import List
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    """Represents a single row in the invoice table."""
    description: str = Field(..., description="Description of goods or services")
    pieces: int = Field(..., description="Number of pieces or quantity")
    weight: str = Field(..., description="Weight of the item (e.g., '100 lbs', '50 kg')")

class BillOfLading(BaseModel):
    """Represents the extracted invoice/BOL data."""
    bol_number: str = Field(..., description="The Bill of Lading or Invoice number")
    date: str = Field(..., description="Date of the document (e.g., YYYY-MM-DD)")
    shipper_name: str = Field(..., description="Name of the shipping company or vendor")
    items: List[LineItem] = Field(..., description="List of line items extracted from the document")
