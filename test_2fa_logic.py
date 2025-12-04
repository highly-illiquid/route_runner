import imaplib
import email
import os
import re
import time
from dotenv import load_dotenv

def test_email_scanner_broad_text():
    load_dotenv()
    
    email_user = (os.environ.get("EMAIL_USER") or "").strip()
    email_pass = (os.environ.get("EMAIL_PASS") or "").strip()
    # Using the subject variable, but searching broadly with TEXT
    infocon_subject = (os.environ.get("INFOCON_SUBJECT") or "").strip()
    
    print(f"Testing BROAD TEXT Scanner for user: '{email_user}'")
    print(f"Searching for UNSEEN emails containing: '{infocon_subject}'")

    try:
        print("Connecting to Gmail...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        
        try:
            mail.select('"[Gmail]/All Mail"')
        except:
            mail.select("inbox")
            
        # BROAD CRITERIA: TEXT match (Header+Body) AND Unread
        criteria = f'(TEXT "{infocon_subject}" UNSEEN)'
        
        for attempt in range(30): # 5 mins
            print(f"[Attempt {attempt+1}/30] Searching UNSEEN (TEXT criteria)...")
            status, messages = mail.search(None, criteria)
            msg_ids = messages[0].split()
            
            if msg_ids:
                # Pick Latest
                last_id = msg_ids[-1]
                _, msg_data = mail.fetch(last_id, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                print(f"\nSUCCESS! Found UNSEEN Email.")
                print(f"Subject: {msg['subject']}")
                print(f"Date:    {msg['date']}")
                
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                    
                match = re.search(r"code.*?(\d{6})", body, re.IGNORECASE | re.DOTALL)
                if match:
                    print(f"CODE: {match.group(1)}")
                    return
                else:
                    print("REGEX FAIL: No code found.")
                    return
            
            time.sleep(10)

        print("\nTIMEOUT: No new UNREAD email arrived matching criteria.")
        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_email_scanner_broad_text()