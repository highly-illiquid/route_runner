import asyncio
import os
import mimetypes
from datetime import datetime
from dotenv import load_dotenv
from src.file_manager import FileManager
from src.ai_extractor import AIExtractor
from src.portal_bot import PortalBot
from src.models import InvoiceBatch

# Global components
file_manager = None
ai_extractor = None
portal_bot = None

async def process_staging():
    """Phase 1: Scan Staging for JSON files and Upload them."""
    print("\n--- Phase 1: Processing Staged Files ---")
    staged_files = file_manager.get_staging_files()
    
    if not staged_files:
        print("No staged files found.")
        return

    print(f"Found {len(staged_files)} staged files.")
    
    for json_path in staged_files:
        print(f"\n>>> Uploading Staged: {json_path.name}")
        try:
            # Load Data
            data_dict = file_manager.read_json(json_path)
            # Convert back to Pydantic model for validation/usage
            batch = InvoiceBatch(**data_dict)
            
            # Upload Loop
            for invoice in batch.invoices:
                print(f"  Processing BOL: {invoice.shippers_bol_number}")
                await portal_bot.upload_invoice(invoice)
            
            # Success -> Archive
            file_manager.promote_to_archive(json_path)
            
        except Exception as e:
            err_msg = f"Upload Failed: {str(e)}"
            print(err_msg)
            file_manager.move_to_quarantine(json_path, err_msg)

async def process_input():
    """Phase 2: Scan Input for New PDFs, Extract, and move to Staging."""
    print("\n--- Phase 2: Processing New Inputs ---")
    input_files = file_manager.get_input_files()
    
    if not input_files:
        print("No new input files found.")
        return

    print(f"Found {len(input_files)} new files.")

    for file_path in input_files:
        print(f"\n>>> Extracting File: {file_path.name}")
        try:
            # Determine Mime Type
            mime_type, _ = mimetypes.guess_type(file_path.name)
            if not mime_type:
                if file_path.suffix.lower() == '.pdf': mime_type = 'application/pdf'
                elif file_path.suffix.lower() in ['.jpg', '.jpeg']: mime_type = 'image/jpeg'
                elif file_path.suffix.lower() == '.png': mime_type = 'image/png'
                else: mime_type = 'application/octet-stream'

            # Read & Extract
            file_bytes = file_manager.read_bytes(file_path)
            batch = ai_extractor.extract_invoice_data(file_bytes, mime_type=mime_type)
            
            # Serialize
            json_data = batch.model_dump_json(indent=2, by_alias=True)
            
            # Save to Staging (and move source file)
            file_manager.save_to_staging(file_path, json_data)
            
        except Exception as e:
            err_msg = f"Extraction Failed: {str(e)}"
            print(err_msg)
            file_manager.move_to_quarantine(file_path, err_msg)

async def main():
    global file_manager, ai_extractor, portal_bot
    load_dotenv()
    print(f"--- Invoice Bot Starting: {datetime.now()} ---")
    
    if not os.environ.get("GEMINI_KEY"):
        print("Error: GEMINI_KEY environment variable is missing.")
        return

    try:
        file_manager = FileManager()
        ai_extractor = AIExtractor()
        portal_bot = PortalBot()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    # Workflow:
    # 1. Clear the 'Outbox' (Staging) first
    await process_staging()
    
    # 2. Process 'Inbox' (Input) -> Staging
    await process_input()
    
    # 3. Clear 'Outbox' again (for the items just processed in step 2)
    await process_staging()

    print("\n--- Run Complete ---")

if __name__ == "__main__":
    asyncio.run(main())