# Entry Point.
# 1. Email Ingestion
# 2. Email Parsing
# 3. (TODO) Duplicate Email Detection
# 4. Email Data Extraction
# 5. Email Classification
# 6. Notification Service

from typing import Dict
from fastapi import FastAPI

from src.email_parser.parser import parse_email
from src.data_extractor.extractor import extract_fields, generate_text_to_process
from src.email_classifier.classifier import classify_email
from src.email_ingestion.ingestion import ingest_email

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


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

    # Step 3: Extract Key Data
    extracted_data = extract_fields(parsed_email)
    text_to_process = generate_text_to_process(parsed_email)
    print("Extraction done.")

    # Step 4: Classify Request Type
    classification = classify_email(parsed_email)

    # Step 5: Send Notifications
    # send_notification()

    # Send the extracted data and classification and email content to the frontend

    return {
        "message": "Email processed successfully!",
        "email_id": parsed_email.email_id,
        "subject": parsed_email.subject,
        "timestamp": parsed_email.timestamp,
        "sender": parsed_email.sender,
        "classification": classification.json(),
        "extracted_data": extracted_data,
        "text_to_process": text_to_process,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
