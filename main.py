import asyncio
import os
import json
import mimetypes
from datetime import datetime
from dotenv import load_dotenv
from src.file_manager import FileManager
from src.email_client import EmailNotifier
from src.ai_extractor import AIExtractor
from src.portal_bot import PortalBot

async def main():
    load_dotenv()
    print(f"--- Invoice Bot Starting: {datetime.now()} ---")
    
    if not os.environ.get("GEMINI_KEY"):
        print("Error: GEMINI_KEY environment variable is missing.")
        return

    try:
        file_manager = FileManager()
        # notifier = EmailNotifier() # Removed per user request
        ai_extractor = AIExtractor()
        portal_bot = PortalBot()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    pending_files = file_manager.get_pending_invoices()
    
    if not pending_files:
        print("No invoices found in 'invoices/input'.")
        return

    print(f"Found {len(pending_files)} files to process.")

    total_bols_processed = 0
    errors = []

    for file_path in pending_files:
        filename = file_path.name
        print(f"\n>>> Processing File: {filename}")
        
        try:
            # Determine Mime Type
            mime_type, _ = mimetypes.guess_type(filename)
            if not mime_type:
                # Fallback defaults
                if filename.lower().endswith('.pdf'):
                    mime_type = 'application/pdf'
                elif filename.lower().endswith(('.jpg', '.jpeg')):
                    mime_type = 'image/jpeg'
                elif filename.lower().endswith('.png'):
                    mime_type = 'image/png'
                else:
                    mime_type = 'application/octet-stream' # Generic fallback

            # Read
            file_bytes = file_manager.read_file(file_path)

            # Extract
            print(f"  Extracting data ({mime_type})...")
            batch = ai_extractor.extract_invoice_data(file_bytes, mime_type=mime_type)
            
            # VERIFICATION: Print the raw JSON (Dump by alias to match expected output)
            json_data = batch.model_dump_json(indent=2, by_alias=True)
            print(f"\n  --- DATA VERIFICATION ({len(batch.invoices)} BOLs found) ---")
            print(json_data)
            print("  --------------------------------------------\n")

            # Upload Loop
            for invoice in batch.invoices:
                print(f"  Processing BOL: {invoice.shippers_bol_number} ({invoice.company_name_from})")
                try:
                    await portal_bot.upload_invoice(invoice)
                    total_bols_processed += 1
                except Exception as e:
                    err = f"Failed BOL {invoice.shippers_bol_number} in {filename}: {e}"
                    print(err)
                    errors.append(err)

            # Archive Success
            archived_path = file_manager.archive_invoice(file_path, success=True)
            
            # SAVE JSON LOG
            file_manager.save_json_record(archived_path, json_data)
            
            print(f"  File archived: {filename}")

        except Exception as e:
            error_msg = f"Failed File {filename}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            file_manager.archive_invoice(file_path, success=False)

    print(f"\n--- Run Complete: {total_bols_processed} BOLs processed ---")
    if errors:
        print("Errors encountered:")
        for e in errors:
            print(f"- {e}")

if __name__ == "__main__":
    asyncio.run(main())
