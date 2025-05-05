# src/emailer.py

from src.utils.email_utils import send_email

def send_email_alert(recipient, subject, message):
    try:
        send_email(recipient, subject, message)
        print(f"Email sent to {recipient} with subject '{subject}'")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")