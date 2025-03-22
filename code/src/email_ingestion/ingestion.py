import imaplib
import email
from email.header import decode_header
import os

def ingest_email():
    """Fetches an email from a configured mailbox."""
    # TODO: Replace with real email fetching (Gmail, Outlook, etc.)
    return {
        "email_id": "123",
        "subject": "Fund Transfer Request",
        "body": "Please transfer $5000 to XYZ account.",
        "attachments": [],
    }

if __name__ == "__main__":
    print(ingest_email())  # For testing
