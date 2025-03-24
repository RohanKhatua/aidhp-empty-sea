from src.models import ParsedEmail, ExtractedData
import spacy
import json
import subprocess
import sys
import re


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


def generate_text_to_process(parsed_email: ParsedEmail) -> str:
    text_to_process = parsed_email.parsed_body

    # Clean up the email body
    text_to_process = re.sub(r"[^a-zA-Z0-9\s]", "", text_to_process)
    text_to_process = re.sub(
        r"\s{2,}", " ", text_to_process
    )  # Remove more than one space
    text_to_process = re.sub(
        r"\n{2,}", "\n", text_to_process
    )  # Remove more than one new line

    attachment_text = "".join(
        attachment.data for attachment in parsed_email.attachments
    )

    text_to_process += attachment_text
    return text_to_process


def extract_fields(parsed_email: ParsedEmail) -> ExtractedData:
    text_to_process = generate_text_to_process(parsed_email)
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
