from models import Attachment, ParsedEmail, Classification
from email_classifier.ensemble import ensemble_classify
from email_classifier.reasoning import get_reasoning


def classify_email(parsed_email: ParsedEmail) -> Classification:
    """
    Determines the request type and subtype based on parsed email content using an ensemble of zero-shot LLMs.

    This function:
      - Combines the email body and attachments.
      - Uses an ensemble of zero-shot classification models (loaded via Hugging Face Transformers)
        to compute probabilities for each candidate category and subcategory.
      - Aggregates the probabilities (weighted as per configuration) to determine the final decision.
      - Uses OpenAI's LLM to generate a detailed reasoning explanation.

    Args:
        parsed_email (ParsedEmail): ParsedEmail object containing email details.

    Returns:
        Classification: An object containing the classification decision and reasoning.
    """
    # Combine email body and attachments
    email_text = parsed_email.parsed_body
    for attachment in parsed_email.attachments:
        email_text += "\n" + attachment.content

    # Get classification decision from the ensemble
    selected_category, selected_subcategory, confidence = ensemble_classify(email_text)

    # Create a decision dictionary for the reasoning module
    decision = {
        "request_type": selected_category,
        "request_subtype": selected_subcategory,
        "confidence": confidence,
    }

    # Generate reasoning using OpenAI's API
    reasoning = get_reasoning(email_text, decision)

    # Return the final classification
    return Classification(
        email_id=parsed_email.email_id,
        request_type=selected_category,
        request_subtype=selected_subcategory,
        confidence=confidence,
        reasoning=reasoning,
    )


if __name__ == "__main__":
    # Example parsed email
    email = ParsedEmail(
        email_id="12345",
        parsed_body="We are terminating our contract. Please transfer the remaining funds to our account.",
        subject="Account Termination",
        timestamp="2025-03-22 12:00:00",
        sender="customer@example.com",
        attachments=[
            Attachment(
                filename="details.txt", content="Transfer details and amounts included."
            )
        ],
    )

    # Classify the email
    classification = classify_email(email)

    # Display the classification results
    print("Classification Result:")
    print(f"Email ID: {classification.email_id}")
    print(f"Request Type: {classification.request_type}")
    print(f"Request Subtype: {classification.request_subtype}")
    print(f"Confidence: {classification.confidence}")
    print(f"Reasoning: {classification.reasoning}")
