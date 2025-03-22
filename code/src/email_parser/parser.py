from src.models import Email, ParsedEmail

def parse_email(email: Email) -> ParsedEmail:
    """Extracts text & key fields from email body & attachments."""
    return ParsedEmail(
        email_id=email.email_id,
        parsed_body=email.body.lower(),
        attachments=email.attachments,
        subject=email.subject,
        timestamp=email.timestamp,
        sender=email.sender,
    )

if __name__ == "__main__":
    sample_email = Email(email_id="123", subject="Test", body="Transfer $5000", attachments=[], timestamp="2023-10-01T12:00:00Z", sender="j")
    print(parse_email(sample_email).model_dump_json()) # For testing
