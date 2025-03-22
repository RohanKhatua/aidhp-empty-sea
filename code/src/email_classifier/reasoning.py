import os
import google.generativeai as genai
import torch
import dotenv  # Used only for checking CUDA availability

dotenv.load_dotenv()

# Configure the Gemini API key (replace with your actual key)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Get from environment variable
genai.configure(api_key=GOOGLE_API_KEY)

# Select the Gemini model
MODEL_NAME = "gemini-2.0-flash"  # Or "gemini-pro-vision" if you have image data
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]


def get_reasoning(email_text: str, decision: dict) -> str:
    """
    Uses the Gemini Pro language model to generate a reasoning explanation
    for the classification decision.

    Args:
        email_text (str): Combined text from email body and attachments.
        decision (dict): Dictionary containing classification decision details.

    Returns:
        str: A reasoning string explaining the decision.
    """

    model = genai.GenerativeModel(MODEL_NAME, safety_settings=SAFETY_SETTINGS)

    # Create a prompt for the model
    prompt = (
        f"Email: {email_text}\n\n"
        f"Classification:\n"
        f"- Request Type: {decision.get('request_type', '')}\n"
        f"- Request Subtype: {decision.get('request_subtype', '')}\n\n"
        f"Explain why this email is classified as this request type and subtype.  Be concise (max 3 sentences)."
    )

    try:
        # Generate the reasoning
        response = model.generate_content(prompt)

        reasoning = response.text.strip()

    except Exception as e:
        reasoning = f"Failed to generate reasoning: {str(e)}"

    return reasoning


# Example usage:
if __name__ == "__main__":
    sample_email = """
    Subject: AU Transfer - Reallocation of Fees

    Hello,

    We need to process a reallocation of fees for the Jones account.
    Please transfer $5,000 from the primary account to the subsidiary.

    Thanks,
    Sarah
    """

    sample_decision = {
        "request_type": "AU Transfer",
        "request_subtype": "Reallocation Fees",
        "confidence": 0.89,
    }

    explanation = get_reasoning(sample_email, sample_decision)
    print(explanation)
