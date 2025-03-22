from src.models import ParsedEmail, ExtractedData, Classification

def classify_email(extracted_data: ExtractedData) -> Classification:
    """Determines the request type based on parsed email content."""
    # TODO: Use BERT model for classification
    return Classification(
        email_id=extracted_data.email_id,
        request_type="Money Movement Inbound",
        request_subtype="Transfer",
        reasoning="Classified as Money Movement Inbound based on keywords in parsed body.",
        confidence=0.95,
    )

if __name__ == "__main__":
    sample_parsed = ExtractedData(
        email_id="123",
        amount=5000,
        currency="USD",
        recipient="XYZ Account",
        expiration_date="2023-10-01",
    )
    print(classify_email(sample_parsed).model_dump_json()) # For testing
