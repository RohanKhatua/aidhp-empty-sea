# Use Python 3.10
FROM python:3.9-slim

WORKDIR /app

# Create a directory to cache Hugging Face models
RUN mkdir -p /root/.cache/huggingface

# Pre-download Hugging Face models and cache them
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('facebook/bart-large-mnli'); \
    AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli'); \
    AutoTokenizer.from_pretrained('MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli'); \
    AutoModelForSequenceClassification.from_pretrained('MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli'); \
    AutoTokenizer.from_pretrained('tasksource/ModernBERT-base-nli'); \
    AutoModelForSequenceClassification.from_pretrained('tasksource/ModernBERT-base-nli')"

# Copy and install dependencies
COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc g++ python3-dev

RUN pip install -r requirements.txt

RUN apt-get purge -y gcc g++ python3-dev && apt-get autoremove -y && apt-get clean

# Copy all project files
COPY . .

# Expose API port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
