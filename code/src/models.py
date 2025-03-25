from pydantic import BaseModel
from typing import List, Optional, Dict


class Attachment(BaseModel):
    fileName: str
    data: str  # Base64 encoded content OR parsed content


# 📩 Email Data Model (Ingestion Output)
class Email(BaseModel):
    email_id: str
    subject: str
    body: str
    timestamp: str  # Format: YYYY-MM-DD HH:MM:SS
    sender: str
    attachments: List[
        Attachment
    ]  # [{ "filename": "file.pdf", "content": "base64string" }]


# 📜 Parsed Email Data Model (Parser Output)
class ParsedEmail(BaseModel):
    email_id: str
    parsed_body: str
    subject: str
    timestamp: str  # Format: YYYY-MM-DD HH:MM:SS
    sender: str
    attachments: List[
        Attachment
    ]  # Same structure as in Email, but with actual parsed "content"


# 📊 Extracted Fields (Data Extraction Output)
class ExtractedData(BaseModel):
    email_id: str
    amount: Optional[float] = None
    currency: Optional[str] = None
    recipient: Optional[str] = None
    expiration_date: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    action_required: Optional[bool] = None
    summary: Optional[str] = None


# 🔍 Classification Output (Classifier Output)
class Classification(BaseModel):
    email_id: str
    request_type: str
    request_subtype: str
    confidence: float
    reasoning: str  # Explanation of classification decision


# 🔔 Notification Model (For sending notifications) This will be sent to n8n or other notif handler.
class NotificationRequest(BaseModel):
    email_id: str
    request_types: List[
        Dict[str, str]
    ]  # [{"type": "Money Movement", "subtype": "Inbound"}]
    teams_to_notify: List[str]  # ["Payments Team", "Operations"]
    status: str  # e.g., "Processed", "Pending", "Failed"
    message: Optional[str] = None  # Optional message for additional context
