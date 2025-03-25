import hashlib
from typing import Dict, Optional
from pymongo import MongoClient
from src.data_extractor.extractor import generate_text_to_process
from src.models import Email, ParsedEmail
from Levenshtein import ratio

def is_similar(text1: str, text2: str, threshold: float = 0.8) -> bool:
    """
    Checks if two strings are similar based on a threshold.

    Args:
        text1 (str): The first string.
        text2 (str): The second string.
        threshold (float): The similarity threshold (default is 0.8).

    Returns:
        bool: True if the strings are similar, False otherwise.
    """
    return ratio(text1, text2) >= threshold

# MongoDB connection setup
MONGO_URI = "mongodb://root:example@mongo:27017/"
client = MongoClient(MONGO_URI)
db = client["emailDB"]
emails_collection = db["emails"]

def generate_email_hash(email: Email) -> str:
    """
    Generates a unique hash for an email based on its normalized content.

    Args:
        email (Email): The email object.

    Returns:
        str: A unique hash representing the email.
    """
    # Normalize subject and body
    normalized_subject = ''.join(e for e in email.subject.lower() if e.isalnum() or e.isspace()).strip()
    normalized_body = ''.join(e for e in email.body.lower() if e.isalnum() or e.isspace()).strip()

    # Combine normalized fields for hash generation
    email_content = f"{email.email_id}|{normalized_subject}|{normalized_body}|{email.sender}"
    for attachment in email.attachments:
        email_content += f"|{attachment.fileName}|{attachment.data}"
    
    # Generate and return the hash
    return hashlib.sha256(email_content.encode()).hexdigest()

def is_duplicate(email: Email, parsed_email: ParsedEmail) -> tuple[Optional[Dict], str]:
    """
    Checks if an email is a duplicate of a previously processed email using fuzzy matching.

    Args:
        email (Email): The email object.

    Returns:
        tuple[Optional[Dict], str]: A tuple containing the original email document if a duplicate is found (or None if not), and the email hash.
    """
    email_hash = generate_email_hash(email)

    # Check for exact hash match
    duplicate_entry = emails_collection.find_one({"hash": email_hash})
    if duplicate_entry:
        return duplicate_entry, email_hash

    # Fuzzy matching: Check for similar emails
    text_to_process = generate_text_to_process(parsed_email)
    for existing_email in emails_collection.find():
        if is_similar(email.subject, existing_email["subject"]) and is_similar(text_to_process, existing_email["text_to_process"]):
            return existing_email, email_hash

    # If no duplicate is found, return None
    return None, email_hash
