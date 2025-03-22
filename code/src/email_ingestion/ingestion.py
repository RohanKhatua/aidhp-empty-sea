from models import Email

def ingest_email() -> Email:
    """Fetches an email from a configured mailbox. Or, from an n8n node as an intermediary."""
    return Email(
        email_id="123",
        subject="Fund Transfer Request",
        body="Please transfer $5000 to XYZ account.",
        timestamp="2023-10-01T12:00:00Z",
        sender="j",
        attachments=[],
    )

if __name__ == "__main__":
    print(ingest_email().model_dump_json())  # For testing
