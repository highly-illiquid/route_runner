import asyncio
import os
from datetime import datetime
from src.file_manager import FileManager
from src.email_client import EmailNotifier
from src.ai_extractor import AIExtractor
from src.portal_bot import PortalBot

async def main():
    print(f"--- Invoice Bot Starting: {datetime.now()} ---")
    
    # Check Critical Env Vars (Gemini is strictly required)
    if not os.environ.get("GEMINI_KEY"):
        print("Error: GEMINI_KEY environment variable is missing.")
        return

    # Initialize Components
    try:
        file_manager = FileManager() # Defaults to invoices/input
        notifier = EmailNotifier()
        ai_extractor = AIExtractor()
        portal_bot = PortalBot()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    # 1. Scan for files
    pending_files = file_manager.get_pending_invoices()
    
    if not pending_files:
        print("No PDF invoices found in 'invoices/input'.")
        return

    print(f"Found {len(pending_files)} invoices to process.")

    success_count = 0
    errors = []

    # 2. Process Loop
    for file_path in pending_files:
        filename = file_path.name
        print(f"\nProcessing {filename}...")
        
        try:
            # Read
            file_bytes = file_manager.read_file(file_path)

            # Extract
            print("  Extracting data...")
            data = ai_extractor.extract_invoice_data(file_bytes)
            print(f"  Extracted: BOL {data.bol_number} from {data.shipper_name}")

            # Upload
            print("  Uploading to portal...")
            await portal_bot.upload_invoice(data)
            
            # Archive Success
            file_manager.archive_invoice(file_path, success=True)
            success_count += 1
            print(f"  Success: {filename}")

        except Exception as e:
            # Archive Failure
            error_msg = f"Failed {filename}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            file_manager.archive_invoice(file_path, success=False)

    # 3. Report
    print("\nGenerating report...")
    notifier.send_summary_email(success_count, errors)
    print("--- Run Complete ---")

if __name__ == "__main__":
    asyncio.run(main())