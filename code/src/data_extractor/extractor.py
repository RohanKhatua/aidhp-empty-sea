from src.models import ParsedEmail
import spacy
import json
import subprocess
import sys


def download_spacy_model(model_name: str):
    try:
        spacy.load(model_name)
    except OSError:
        print(f"Model '{model_name}' not found. Downloading...")
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name])
        print(f"Model '{model_name}' downloaded successfully.")


def spacy_extract_with_labels(text):
    model_name = "en_core_web_md"
    download_spacy_model(model_name)

    # Load model
    nlp = spacy.load(model_name)

    # Get and print available entity types
    ner = nlp.get_pipe("ner")
    labels = set(ner.labels)
    # print("SpaCy Recognizable Entity Types:")
    # print("\n".join(f"- {label}" for label in sorted(labels)))
    # print("\n" + "=" * 50 + "\n")

    # Process text
    doc = nlp(text)
    return [
        {
            "entity": ent.text,
            "label": ent.label_,
            "start_idx": ent.start_char,
            "end_idx": ent.end_char,
        }
        for ent in doc.ents
    ]


def extract_fields(parsed_email: ParsedEmail) -> dict[str, str]:

    text_to_process = (
        f"Subject: {parsed_email.subject}\nBody: {parsed_email.parsed_body}"
    )

    attachment_text = "".join(
        attachment.data for attachment in parsed_email.attachments
    )

    text_to_process += attachment_text

    # text_to_process now contains the subject, body, and all attachment data
    # We can now use a NLP model to extract structured data from this text

    extracted_data = spacy_extract_with_labels(text_to_process)
    return extracted_data


if __name__ == "__main__":
    sample_parsed = ParsedEmail(
        email_id="123",
        parsed_body="Transfer $5000 to XYZ",
        attachments=[],
        subject="Test",
        timestamp="2023-10-01T12:00:00Z",
        sender="j",
    )
    extracted_fields = extract_fields(sample_parsed)
    print(json.dumps(extracted_fields, indent=4))  # For testing
