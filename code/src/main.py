# Entry Point.
# 1. Email Ingestion
# 2. Email Parsing
# 3. (TODO) Duplicate Email Detection
# 4. Email Data Extraction
# 5. Email Classification
# 6. Notification Service

from typing import Dict
from fastapi import FastAPI
from pymongo import MongoClient

from src.email_classifier.config_reader import load_notification_mapping
from src.duplicate_checker.duplicate_checker import is_duplicate
from src.email_parser.parser import parse_email
from src.data_extractor.extractor import extract_fields, generate_text_to_process
from src.email_classifier.classifier import classify_email
from src.email_ingestion.ingestion import ingest_email

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# MongoDB connection setup
MONGO_URI = "mongodb://root:example@mongo:27017/"
client = MongoClient(MONGO_URI)
db = client["emailDB"]
emails_collection = db["emails"]

@app.post("/process-email")
def process_email(raw_email: Dict):
    """
    API endpoint for processing an email end-to-end.
    - Ingests email
    - Parses content
    - Extracts key data
    - Classifies request type
    - Sends notifications
    """
    print("Processing email...")
    print(raw_email)
    # Step 1: Ingest Email
    email = ingest_email(raw_email)

    # Step 2: Parse Email
    parsed_email = parse_email(email)

    duplicate_info, email_hash = is_duplicate(email, parsed_email)
    if duplicate_info:
        return {
            "message": "Duplicate email detected. Skipping processing.",
            "duplicate_email": {
                "email_id": duplicate_info["email_id"],
                "subject": duplicate_info["subject"],
                "timestamp": duplicate_info["timestamp"],
                "sender": duplicate_info["sender"],
            },
        }

    # Step 3: Extract Key Data
    extracted_data = extract_fields(parsed_email)
    text_to_process = generate_text_to_process(parsed_email)
    print("Extraction done.")

    # Step 4: Classify Request Type
    classification = classify_email(parsed_email)

    # Step 5: Send Notifications
    # send_notification()
    category = classification.request_type
    subcategory = classification.request_subtype
    recipients = load_notification_mapping().get(category, [])

    # Send the extracted data and classification and email content to the frontend
    return {
        "message": "Email processed successfully!",
        "hash": email_hash,
        "email_id": parsed_email.email_id,
        "subject": parsed_email.subject,
        "timestamp": parsed_email.timestamp,
        "sender": parsed_email.sender,
        "classification": classification,
        "extracted_data": extracted_data,
        "text_to_process": text_to_process,
        "recipients": recipients,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
