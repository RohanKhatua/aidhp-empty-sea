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
from src.data_extractor.extractor import extract_fields
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
    # email = ingest_email(raw_email.dict())
    email = ingest_email(raw_email)

    # Step 2: Parse Email
    parsed_email = parse_email(email)
    # print(parsed_email.model_dump())

    # Step 3: Extract Key Data
    extracted_data = extract_fields(parsed_email)
    print("Extraction done.")

    # Step 4: Classify Request Type
    classification = classify_email(parsed_email)
    # print(classification.json(indent=4))
    # print("Classification Result:")
    # print(classification.reasoning)

    # Step 5: Send Notifications
    # send_notification()

    # Send the extracted data and classification and email content to the frontend

    return {
        "message": "Email processed successfully!",
        "classification": classification.json(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
