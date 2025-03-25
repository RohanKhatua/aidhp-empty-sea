from src.models import Email, ParsedEmail, Attachment
import re
from .utils import parse_attachments

def parse_email(email: Email) -> ParsedEmail:
    """Extracts text & key fields from email body & attachments."""

    body = email.body
    cleaned_body = re.sub(r'\s+', ' ', body).strip() #removing \n new line symbols and extra spaces
    parsed_attachments = parse_attachments(email.attachments)

    return ParsedEmail(
        email_id=email.email_id,
        parsed_body=cleaned_body.lower(),
        attachments=parsed_attachments,
        subject=email.subject,
        timestamp=email.timestamp,
        sender=email.sender,
    )

if __name__ == "__main__":
    sample_email = Email(email_id="123", 
                         subject="Test", 
                         body="       Transfer $5000 \n who is the best", 
                         attachments=[
                  
                         ], 
                         timestamp="2023-10-01T12:00:00Z", 
                         sender="j")


    
    print(parse_email(sample_email).model_dump_json()) # For testing
