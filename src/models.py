from typing import List, Optional, Union
from pydantic import BaseModel, Field

class ConsigneeInfo(BaseModel):
    name: Optional[str] = Field(None, alias="NAME")
    address: Optional[str] = Field(None, alias="ADDRESS")
    phone: Optional[str] = Field(None, alias="PHONE")

class ShipmentDetail(BaseModel):
    description: Optional[str] = Field(None, alias="DESCRIPTION")
    pieces: Optional[int] = Field(None, alias="PIECES")
    weight: Optional[int] = Field(None, alias="WEIGHT")
    shipper_refs: Optional[List[str]] = Field(None, alias="SHIPPER'S_REFERENCE")
    consignee_pos: Optional[List[str]] = Field(None, alias="CONSIGNEE'S_PO")
    packing_list: Optional[str] = Field(None, alias="PACKING_LIST")

class ConsigneeReceiptInfo(BaseModel):
    print_name: Optional[str] = Field(None, alias="PRINT_NAME")
    date: Optional[str] = Field(None, alias="DATE")
    pieces_received: Optional[Union[int, str]] = Field(None, alias="PIECES_RECEIVED")
    time_eta: Optional[str] = Field(None, alias="TIME_ETA")

class BillOfLading(BaseModel):
    shippers_bol_number: str = Field(..., alias="SHIPPERS_BOL#", description="The Bill of Lading or Invoice number")
    date: str = Field(..., alias="DATE")
    company_name_from: str = Field(..., alias="COMPANY_NAME_FROM")
    address_from: str = Field(..., alias="ADDRESS_FROM")
    carrier_scac: Optional[str] = Field(None, alias="CARRIER_SCAC")
    pallets: Optional[Union[int, str]] = Field(None, alias="PALLETS")
    consigned_to_code: Optional[str] = Field(None, alias="CONSIGNED_TO_CODE")
    consignee_info: ConsigneeInfo = Field(..., alias="CONSIGNEE_INFO")
    osad_email: Optional[str] = Field(None, alias="OSAD_EMAIL")
    billable_accessorials: List[str] = Field(default_factory=list, alias="BILLABLE_ACCESSORIALS")
    freight_status: Optional[str] = Field(None, alias="FREIGHT_STATUS")
    special_delivery_instructions: Optional[str] = Field(None, alias="SPECIAL_DELIVERY_INSTRUCTIONS")
    shipment_details: List[ShipmentDetail] = Field(..., alias="SHIPMENT_DETAILS")
    consignee_receipt_info: Optional[ConsigneeReceiptInfo] = Field(None, alias="CONSIGNEE_RECEIPT_INFO")

class InvoiceBatch(BaseModel):
    invoices: List[BillOfLading] = Field(..., description="All distinct Bill of Ladings found in the file")
