import os
import re
from collections import Counter
from typing import Dict, List, Tuple, Optional
from transformers import pipeline, BertTokenizer, AutoModel
import torch
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity
from src.email_classifier.config_reader import load_categories_config, load_model_config
import yaml
from pathlib import Path

# Load categories and subcategories from the YAML file


# Load the configuration
CATEGORIES, SUBCATEGORIES = load_categories_config()

# Create combined labels for classification
COMBINED_LABELS = []
for category in CATEGORIES:
    if category in SUBCATEGORIES and SUBCATEGORIES[category]:
        for subcategory in SUBCATEGORIES[category]:
            COMBINED_LABELS.append(f"{category} - {subcategory}")
    else:
        COMBINED_LABELS.append(category)

# Create combined labels for classification
COMBINED_LABELS = []
for category in CATEGORIES:
    if category in SUBCATEGORIES and SUBCATEGORIES[category]:
        for subcategory in SUBCATEGORIES[category]:
            COMBINED_LABELS.append(f"{category} - {subcategory}")
    else:
        COMBINED_LABELS.append(category)

# Cache for models and embeddings
_pipeline_cache = {}
_embedding_model_cache = {}
_label_embeddings_cache = {}
_keyword_patterns = {}


def get_pipeline(model_name: str):
    """
    Retrieves or loads the zero-shot classification pipeline for the given model.

    Args:
        model_name (str): The Hugging Face model name.

    Returns:
        pipeline: A Hugging Face zero-shot classification pipeline.
    """
    if model_name not in _pipeline_cache:
        # Use AutoTokenizer to explicitly load the appropriate tokenizer
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

        _pipeline_cache[model_name] = pipeline(
            "zero-shot-classification", model=model_name, tokenizer=tokenizer
        )
    return _pipeline_cache[model_name]


def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Loads or retrieves a cached sentence embedding model.

    Args:
        model_name (str): Name of the sentence transformer model.

    Returns:
        tuple: (tokenizer, model) for generating embeddings.
    """
    if model_name not in _embedding_model_cache:
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        _embedding_model_cache[model_name] = (tokenizer, model)
    return _embedding_model_cache[model_name]


def get_label_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Generates and caches embeddings for all category and combined labels.

    Args:
        model_name (str): Name of the sentence transformer model.

    Returns:
        dict: Dictionary mapping labels to their embeddings.
    """
    if model_name not in _label_embeddings_cache:
        tokenizer, model = get_embedding_model(model_name)

        # Create descriptive phrases for each label to improve embedding quality
        label_descriptions = {}
        for label in COMBINED_LABELS:
            if " - " in label:
                category, subcategory = label.split(" - ", 1)
                label_descriptions[label] = (
                    f"Email about {subcategory} related to {category}"
                )
            else:
                label_descriptions[label] = f"Email about {label}"

        # Generate embeddings for each label description
        embeddings = {}
        for label, description in label_descriptions.items():
            embeddings[label] = generate_embedding(description, tokenizer, model)

        _label_embeddings_cache[model_name] = embeddings

    return _label_embeddings_cache[model_name]


def generate_embedding(text: str, tokenizer, model):
    """
    Generates a sentence embedding for the input text.

    Args:
        text (str): Text to embed.
        tokenizer: Transformer tokenizer.
        model: Transformer model.

    Returns:
        numpy.ndarray: Embedding vector.
    """
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # Use mean pooling to get sentence embedding
    attention_mask = inputs["attention_mask"]
    token_embeddings = outputs.last_hidden_state
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embedding = sum_embeddings / sum_mask

    return embedding.detach().numpy()[0]


def preprocess_text(text: str) -> str:
    """
    Preprocesses email text to improve classification.

    Args:
        text (str): Original email text.

    Returns:
        str: Cleaned and preprocessed text.
    """
    # Remove email headers if present
    text = re.sub(
        r"^(From|To|Cc|Subject|Date|Sent):.+?(\n|$)",
        "",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove email signatures (common patterns)
    text = re.sub(r"(?i)best regards[\s\S]*?$", "", text)
    text = re.sub(r"(?i)sincerely[\s\S]*?$", "", text)
    text = re.sub(r"(?i)thank you[\s\S]*?$", "", text)

    # Remove redundant whitespace and newlines
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_keywords(text: str) -> Dict[str, List[str]]:
    """
    Extracts domain-specific keywords from the text that might indicate certain categories.

    Args:
        text (str): Preprocessed email text.

    Returns:
        Dict: Dictionary mapping categories to found keywords.
    """
    # Initialize keyword patterns if not already done
    if not _keyword_patterns:
        _keyword_patterns.update(
            {
                "AU Transfer": [
                    r"\b(?:au|authorized user)\s+(?:transfer|reallocation)\b",
                    r"\breallocation\s+(?:fee|principal)\b",
                    r"\bamendment\s+fee\b",
                ],
                "Closing Notice": [
                    r"\bclos(?:e|ing)\s+notice\b",
                    r"\bcashless\s+roll\b",
                    r"\b(?:increase|decrease)\s+(?:notice|notification)\b",
                    r"\bletter\s+of\s+credit\s+fee\b",
                    r"\bongoing\s+fee\b",
                ],
                "Commitment Change": [
                    r"\bcommitment\s+(?:change|increase|modification)\b"
                ],
                "Fee Payment": [
                    r"\bfee\s+payment\b",
                    r"\b(?:principal|interest)\s+payment\b",
                    r"\bprincipal\s+(?:and|&|\+)\s+interest\b",
                ],
                "Money Movement": [
                    r"\bmoney\s+movement\b",
                    r"\b(?:inbound|outbound)\s+(?:transfer|payment)\b",
                    r"\bforeign\s+currency\b",
                    r"\btimebound\b",
                ],
                "Adjustment": [
                    r"\badjustment\b",
                    r"\bcorrection\b",
                    r"\bmodification\b",
                ],
            }
        )

    results = {}

    # Search for each keyword pattern
    for category, patterns in _keyword_patterns.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            if found:
                matches.extend(found)

        if matches:
            results[category] = matches

    return results


def ensemble_classify(
    email_text: str, config_path: str = "src/email_classifier/config/models_config.yaml"
) -> tuple:
    """
    Enhanced ensemble classification using multiple NLP techniques:
    1. Text preprocessing
    2. Zero-shot classification
    3. Semantic similarity with sentence embeddings
    4. Keyword extraction
    5. Ensemble weighting

    Args:
        email_text (str): Combined text from email body and attachments.
        config_path (str): Path to configuration file containing model details.

    Returns:
        Tuple:
          - selected_category (str): Final predicted request type.
          - selected_subcategory (str): Final predicted request subtype (if applicable).
          - confidence (float): Confidence of the prediction.
    """
    # Load model configuration
    config = load_model_config(config_path)
    model_configs = config.get("models", [])

    # Preprocess the email text
    processed_text = preprocess_text(email_text)

    # Initialize score aggregation
    aggregated_scores = {label: 0.0 for label in COMBINED_LABELS}
    total_weight = 0.0

    # 1. Zero-shot classification from multiple models
    for model in model_configs:
        model_name = model.get("name")
        weight = model.get("weight", 1.0)
        total_weight += weight
        classifier = get_pipeline(model_name)

        # Zero-shot classification for combined labels
        result = classifier(
            processed_text, candidate_labels=COMBINED_LABELS, multi_label=False
        )
        model_probs = {
            label: score for label, score in zip(result["labels"], result["scores"])
        }

        for label in COMBINED_LABELS:
            aggregated_scores[label] += model_probs.get(label, 0.0) * weight

    # 2. Semantic similarity with sentence embeddings
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer, model = get_embedding_model(embedding_model_name)
    label_embeddings = get_label_embeddings(embedding_model_name)

    # Generate embedding for the email text
    email_embedding = generate_embedding(processed_text, tokenizer, model)

    # Calculate similarity scores with all labels
    similarity_scores = {}
    for label, label_embedding in label_embeddings.items():
        similarity = cosine_similarity([email_embedding], [label_embedding])[0][0]
        similarity_scores[label] = similarity

        # Add similarity scores to aggregated scores with a weight
        similarity_weight = 0.7  # Can be adjusted based on performance
        aggregated_scores[label] += similarity * similarity_weight
        total_weight += similarity_weight

    # 3. Keyword-based classification
    keywords = extract_keywords(processed_text)
    if keywords:
        keyword_weight = 0.5  # Can be adjusted based on performance
        total_weight += keyword_weight

        # Distribute keyword weight among found categories
        for category, found_keywords in keywords.items():
            # Find relevant labels for this category
            relevant_labels = [
                label
                for label in COMBINED_LABELS
                if label.startswith(category) or label == category
            ]

            if relevant_labels:
                # Weight by number of keyword matches
                weight_per_label = (keyword_weight * len(found_keywords)) / len(
                    relevant_labels
                )
                for label in relevant_labels:
                    aggregated_scores[label] += weight_per_label

    # Normalize aggregated scores by total weight
    for label in aggregated_scores:
        aggregated_scores[label] /= total_weight

    # Determine the label with the highest aggregated score
    selected_combined_label = max(aggregated_scores, key=aggregated_scores.get)
    confidence = aggregated_scores[selected_combined_label]

    # Split the combined label back into category and subcategory
    if " - " in selected_combined_label:
        selected_category, selected_subcategory = selected_combined_label.split(
            " - ", 1
        )
    else:
        selected_category = selected_combined_label
        selected_subcategory = ""

    return selected_category, selected_subcategory, confidence
