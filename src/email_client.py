import smtplib
import os
from email.mime.text import MIMEText
from typing import List

class EmailNotifier:
    def __init__(self):
        self.email_user = os.environ.get("EMAIL_USER")
        self.email_pass = os.environ.get("EMAIL_PASS")
        self.notify_email = os.environ.get("NOTIFY_EMAIL")
        
        # Check if email functionality is configured
        self.enabled = all([self.email_user, self.email_pass, self.notify_email])
        if not self.enabled:
            print("Warning: Email notifications disabled (missing env vars).")

    def send_summary_email(self, processed_count: int, errors: List[str]):
        """
        Sends a summary report via SMTP.
        """
        if not self.enabled:
            return

        # Don't send email if nothing happened and no errors
        if processed_count == 0 and not errors:
            return

        subject = f"Invoice Bot Report: {processed_count} Processed"
        body = f"Run report.\n\nProcessed: {processed_count} invoices.\n"
        
        if errors:
            subject += " [HAS ERRORS]"
            body += "\nErrors encountered:\n" + "\n".join(f"- {e}" for e in errors)
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = self.notify_email

        print("Sending summary email...")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            print("Summary email sent.")
        except Exception as e:
            print(f"SMTP Error: {e}")
