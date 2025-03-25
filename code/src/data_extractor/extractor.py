from typing import Optional, Dict, Any
import re
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import base64
from dotenv import load_dotenv
from os import getenv

from src.models import Attachment, ParsedEmail, ExtractedData

load_dotenv()

GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")  # Get from environment variable
genai.configure(api_key=GOOGLE_API_KEY)


def extract_from_attachments(parsed_email: ParsedEmail) -> Dict[str, Any]:
    """Extract information from email attachments."""

    extracted_data = {}

    for attachment in parsed_email.attachments:
        # Try to decode if it's base64 encoded
        try:
            content = base64.b64decode(attachment.data).decode("utf-8")
        except:
            # If decoding fails, assume it's already parsed content
            content = attachment.data

        # Look for amounts in attachments
        if not extracted_data.get("amount"):
            amount_pattern = r"(\$|€|£|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)"
            amount_match = re.search(amount_pattern, content)

            if amount_match:
                if amount_match.group(1):
                    currency_symbols = {"$": "USD", "€": "EUR", "£": "GBP", "₹": "INR"}
                    extracted_data["currency"] = currency_symbols.get(
                        amount_match.group(1), "USD"
                    )
                amount_str = amount_match.group(2)
                extracted_data["amount"] = float(amount_str.replace(",", ""))

        # Look for dates in attachments
        if not extracted_data.get("expiration_date"):
            date_pattern = (
                r"expir(?:es?|ation)\s+(?:date|on)?\s*:?\s*(\d{4}-\d{2}-\d{2})"
            )
            date_match = re.search(date_pattern, content, re.IGNORECASE)
            if date_match:
                extracted_data["expiration_date"] = date_match.group(1)

    return extracted_data


def extract_fields_with_genai(parsed_email: ParsedEmail) -> Dict[str, Any]:
    """Extracts structured data using Gemini 2.0 Flash."""

    genai.configure(api_key=GOOGLE_API_KEY)

    # Set up the model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=GenerationConfig(
            temperature=0.1,
            top_p=0.95,
            top_k=40,
        ),
    )

    # Define the list of allowed recipients
    allowed_recipients = [
        "Customer Service",
        "Account Management",
        "Loan Department",
        "Fraud Prevention",
        "Marketing Team",
        "Compliance Department",
        "Investment Services",
        "Online Banking Support",
        "Credit Card Services",
        "Wealth Management",
        "Business Banking",
    ]

    # allowed catagories of different teams
    allowed_catagories = [
        "Customer Service",
        "Account Management",
        "Transaction Support",
        "Card Services",
        "Digital Banking Support",
        "Marketing Team",
        "Notifications Department",
        "Customer Engagement",
        "Loan Department",
        "Mortgage Services",
        "Investment Services",
        "Wealth Management",
        "Fraud Prevention",
        "Compliance Department",
        "Technical Support",
        "Insurance Services",
        "Foreign Exchange",
        "Business Banking",
        "Private Banking",
        "Branch Operations",
        "ATM Services",
        "Mobile Banking Support",
        "Online Banking Support",
        "Credit Card Services",
        "Debit Card Services",
        "Statement Services",
        "Payment Processing",
        "Treasury Services",
        "Tax Services",
        "Estate Planning",
    ]

    # Process attachments for additional context
    attachment_text = ""
    for attachment in parsed_email.attachments:
        try:
            content = base64.b64decode(attachment.data).decode("utf-8")
            attachment_text += f"\nAttachment {attachment.fileName}:\n{content}\n"
        except:
            # If decoding fails, assume it's already parsed content
            attachment_text += (
                f"\nAttachment {attachment.fileName}:\n{attachment.data}\n"
            )

    # Update the prompt to include the list of allowed recipients and attachments
    prompt = f"""
    Extract the following information from this email:
    
    Email subject: {parsed_email.subject}
    Email sender: {parsed_email.sender}
    Email date: {parsed_email.timestamp}
    Email body:
    {parsed_email.parsed_body}
    
    {attachment_text}
    
    Answer with ONLY the requested information in this EXACT format:
    AMOUNT: [the monetary amount as a number without currency symbol, or "null" if not found]
    CURRENCY: [the currency code (USD, EUR, GBP, INR, etc.), or "null" if not found]
    RECIPIENT: [based on the email the team receiving the email, MUST be one of these: {', '.join(allowed_recipients)},]
    EXPIRATION_DATE: [any expiration date in YYYY-MM-DD format, or "null" if not found]
    PRIORITY: [high, medium, or low, or "null" if not found]
    CATEGORY: [the category of the email MUST be one of these: {', '.join(allowed_catagories)}, or "null" if not found]
    ACTION_REQUIRED: [true or false, or "null" if not found]
    SUMMARY: [a brief summary of the email content in 1-2 sentences]
    """

    try:
        response = model.generate_content(prompt)

        # Parse the structured text response
        result = {}
        text = response.text

        # Extract each field using regex
        amount_match = re.search(r"AMOUNT:\s*([^\n]+)", text)
        result["amount"] = (
            None
            if amount_match is None or amount_match.group(1).strip() == "null"
            else float(amount_match.group(1).strip())
        )

        currency_match = re.search(r"CURRENCY:\s*([^\n]+)", text)
        result["currency"] = (
            None
            if currency_match is None or currency_match.group(1).strip() == "null"
            else currency_match.group(1).strip()
        )

        recipient_match = re.search(r"RECIPIENT:\s*([^\n]+)", text)
        recipient = (
            None
            if recipient_match is None or recipient_match.group(1).strip() == "null"
            else recipient_match.group(1).strip()
        )
        # Ensure the recipient is in the allowed list
        result["recipient"] = recipient if recipient in allowed_recipients else None

        date_match = re.search(r"EXPIRATION_DATE:\s*([^\n]+)", text)
        result["expiration_date"] = (
            None
            if date_match is None or date_match.group(1).strip() == "null"
            else date_match.group(1).strip()
        )

        priority_match = re.search(r"PRIORITY:\s*([^\n]+)", text)
        result["priority"] = (
            None
            if priority_match is None or priority_match.group(1).strip() == "null"
            else priority_match.group(1).strip()
        )

        category_match = re.search(r"CATEGORY:\s*([^\n]+)", text)
        result["category"] = (
            None
            if category_match is None or category_match.group(1).strip() == "null"
            else category_match.group(1).strip()
        )

        action_match = re.search(r"ACTION_REQUIRED:\s*([^\n]+)", text)
        action_text = (
            None
            if action_match is None or action_match.group(1).strip() == "null"
            else action_match.group(1).strip().lower()
        )
        result["action_required"] = (
            True
            if action_text == "true"
            else (False if action_text == "false" else None)
        )

        summary_match = re.search(r"SUMMARY:\s*(.+)(?:\n|$)", text, re.DOTALL)
        result["summary"] = (
            None
            if summary_match is None or summary_match.group(1).strip() == "null"
            else summary_match.group(1).strip()
        )

        return result

    except Exception as e:
        print(f"Error extracting data with Gemini: {e}")
        return {}


def extract_fields_with_regex(parsed_email: ParsedEmail) -> ExtractedData:
    """Extracts structured data using regex patterns."""

    # Extract amount and currency
    amount_pattern = r"(\$|€|£|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)"
    amount_match = re.search(amount_pattern, parsed_email.parsed_body)

    amount: Optional[float] = None
    currency: Optional[str] = None

    if amount_match:
        if amount_match.group(1):
            currency_symbols = {"$": "USD", "€": "EUR", "£": "GBP", "₹": "INR"}
            currency = currency_symbols.get(amount_match.group(1), "USD")
        amount_str = amount_match.group(2)
        amount = float(amount_str.replace(",", ""))

    # Extract recipient
    recipient_pattern = r"to\s+([A-Za-z0-9\s]+)"
    recipient_match = re.search(recipient_pattern, parsed_email.parsed_body)
    recipient = recipient_match.group(1).strip() if recipient_match else None

    # Extract expiration date (if available)
    date_pattern = r"expir(?:es?|ation)\s+(?:date|on)?\s*:?\s*(\d{4}-\d{2}-\d{2})"
    date_match = re.search(date_pattern, parsed_email.parsed_body, re.IGNORECASE)
    expiration_date = date_match.group(1) if date_match else None

    return ExtractedData(
        email_id=parsed_email.email_id,
        amount=amount,
        currency=currency,
        recipient=recipient,
        expiration_date=expiration_date,
    )


def extract_with_spacy(parsed_email: ParsedEmail) -> Dict[str, Any]:
    """Extract entities using spaCy as a fallback or enhancement."""

    return {}

    # # Load spaCy model
    # nlp = spacy.load("en_core_web_sm")

    # # Process the email text
    # doc = nlp(parsed_email.parsed_body)

    # extracted_data = {}

    # # Extract entities
    # for ent in doc.ents:
    #     if ent.label_ == "MONEY":
    #         # Try to extract amount and currency
    #         money_text = ent.text
    #         currency_match = re.search(r"(\$|€|£|₹|USD|EUR|GBP|INR)", money_text)
    #         amount_match = re.search(r"(\d+(?:,\d+)*(?:\.\d+)?)", money_text)

    #         if amount_match:
    #             extracted_data["amount"] = float(amount_match.group(1).replace(",", ""))

    #         if currency_match:
    #             currency_symbols = {"$": "USD", "€": "EUR", "£": "GBP", "₹": "INR"}
    #             extracted_data["currency"] = currency_symbols.get(
    #                 currency_match.group(1), currency_match.group(1)
    #             )

    #     elif ent.label_ == "DATE":
    #         # Check if this might be an expiration date
    #         if "expir" in parsed_email.parsed_body.lower():
    #             # Try to convert to YYYY-MM-DD format
    #             try:
    #                 from dateutil import parser

    #                 date_obj = parser.parse(ent.text)
    #                 extracted_data["expiration_date"] = date_obj.strftime("%Y-%m-%d")
    #             except:
    #                 pass

    #     elif ent.label_ == "PERSON":
    #         # Could be recipient
    #         if "recipient" not in extracted_data:
    #             extracted_data["recipient"] = ent.text

    # return extracted_data


def extract_fields(parsed_email: ParsedEmail) -> ExtractedData:
    """Combines all extraction methods for the best results."""

    # Get data from regex patterns
    regex_data = extract_fields_with_regex(parsed_email)

    # Get data from Gemini
    genai_data = extract_fields_with_genai(parsed_email)

    # Get data from spaCy as fallback
    spacy_data = extract_with_spacy(parsed_email)

    # Get data from attachments
    attachment_data = extract_from_attachments(parsed_email)

    # Merge all data sources, prioritizing in this order: regex > gemini > spacy > attachments
    merged_data = {
        "email_id": parsed_email.email_id,
        "amount": regex_data.amount
        or genai_data.get("amount")
        or spacy_data.get("amount")
        or attachment_data.get("amount"),
        "currency": regex_data.currency
        or genai_data.get("currency")
        or spacy_data.get("currency")
        or attachment_data.get("currency"),
        "recipient": genai_data.get("recipient")
        or regex_data.recipient
        or spacy_data.get("recipient"),
        "expiration_date": genai_data.get("expiration_date")
        or regex_data.expiration_date
        or spacy_data.get("expiration_date")
        or attachment_data.get("expiration_date"),
        "priority": genai_data.get("priority"),
        "category": genai_data.get("category"),
        "action_required": genai_data.get("action_required"),
        "summary": genai_data.get("summary"),
    }

    return ExtractedData(**merged_data)


if __name__ == "__main__":

    # Example usage
    email = ParsedEmail(
        email_id="123",
        parsed_body="Please transfer $500.00 to John Doe. The offer expires on 2025-04-15.",
        subject="Payment Request",
        timestamp="2025-03-22 10:30:45",
        sender="finance@example.com",
        attachments=[
            Attachment(
                fileName="invoice.txt",
                data=base64.b64encode(
                    "Invoice #12345\nAmount: $500.00\nDue Date: 2025-04-15".encode()
                ).decode(),
            )
        ],
    )

    extracted_data = extract_fields(email)
    print(extracted_data)
