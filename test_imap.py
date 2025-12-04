import imaplib
import email
import os
from dotenv import load_dotenv

def test_imap():
    load_dotenv()
    
    user = (os.environ.get("EMAIL_USER") or "").strip()
    password = (os.environ.get("EMAIL_PASS") or "").strip()
    target_sender = (os.environ.get("INFOCON_EMAIL") or "").strip()
    
    print(f"Testing IMAP for user: '{user}'")
    if target_sender:
        print(f"Searching for emails from: '{target_sender}'")
    else:
        print("Warning: INFOCON_EMAIL not set. Searching ALL mail.")

    try:
        print("Connecting to imap.gmail.com...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        
        print("Logging in...")
        mail.login(user, password)
        print("Login SUCCESS!")
        
        print("Selecting Inbox...")
        mail.select("inbox")
        
        # Build Search Criteria
        if target_sender:
            criteria = f'(FROM "{target_sender}")'
        else:
            criteria = 'ALL'
            
        print(f"Searching with criteria: {criteria}")
        status, messages = mail.search(None, criteria)
        
        msg_ids = messages[0].split()
        
        if not msg_ids:
            print("No emails found matching criteria.")
        else:
            print(f"Found {len(msg_ids)} emails.")
            last_id = msg_ids[-1]
            
            status, msg_data = mail.fetch(last_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            print(f"\n--- Latest Match ---")
            print(f"Subject: {msg['subject']}")
            print(f"From: {msg['from']}")
            print(f"Date: {msg['date']}")
            print("--------------------")
        
        mail.close()
        mail.logout()
        print("\nTest Complete.")
        
    except Exception as e:
        print(f"\nIMAP TEST FAILED: {e}")

if __name__ == "__main__":
    test_imap()