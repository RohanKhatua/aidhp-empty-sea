from src.models import ParsedEmail, ExtractedData

def extract_fields(parsed_email: ParsedEmail) -> ExtractedData:
    """Extracts structured data (amount, date, etc.)."""
    return ExtractedData(
        email_id=parsed_email.email_id,
        amount=5000,
        currency="USD",
        recipient="XYZ Account",
    )

if __name__ == "__main__":
    sample_parsed = ParsedEmail(email_id="123", parsed_body="Transfer $5000 to XYZ", attachments=[], subject="Test", timestamp="2023-10-01T12:00:00Z", sender="j")
    print(extract_fields(sample_parsed).model_dump_json()) # For testing
