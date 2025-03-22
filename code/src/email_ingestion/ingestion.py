from typing import Dict
from src.models import Email

def ingest_email(raw_email: Dict) -> Email:
    """Fetches an email from a configured mailbox. Or, from an n8n node as an intermediary."""

    # attachments are currently a list of dicts with properties fileName and data. Convert to having file
    return Email(
        email_id=raw_email.get("messageId", "123"),
        subject=raw_email.get("subject", "Test"),
        body=raw_email.get("body", "Transfer $5000"),
        timestamp=raw_email.get("date", "2023-10-01T12:00:00Z"),
        sender=raw_email.get("from", "j@j.com"),
        attachments = raw_email.get("attachments", [])
    )

if __name__ == "__main__":
    print(ingest_email({}).model_dump_json())  # For testing
