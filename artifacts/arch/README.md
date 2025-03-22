# Architecture Documentation

## High Level Overview

- Email Ingestion Node -> Processing Black Box -> Email Notification Node.
- The Processing Black Box has the following components:
  - Email Ingestion Handler
  - Email and Attachment Parser
  - Email Data Extractor
  - Email Category Classifier
  - Email Notification Generator
- The API contract between the Ingestion Node and the Black Box is as follows:
```
POST /process-email
Content-Type: application/json

{
  "sender": "user@example.com",
  "subject": "Payment Request",
  "body": "Please process payment of $5,000 for Deal XYZ.",
  "timestamp": "2025-03-21T10:30:00Z",
  "attachments": [
    {
      "filename": "invoice.pdf",
      "content": "JVBERi0xLjUK...",  # Base64 encoded
      "mime_type": "application/pdf"
    }
  ]
}
```
- The API contract between the Black Box and the Notification Node is as follows (to be confirmed):
```
{
  "status": "processed",
  "classification": {
    "request_type": "Money Movement Inbound",
    "sub_request_type": "Principal + Interest"
  },
  "notification": {
    "teams_to_notify": ["Payments Team", "Finance Ops"],
    "message": "New Money Movement Inbound request from user@example.com"
  }
}
```
