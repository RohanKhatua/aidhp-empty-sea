# Entry Point.
# 1. Email Ingestion
# 2. Email Parsing
# 3. (TODO) Duplicate Email Detection
# 4. Email Data Extraction
# 5. Email Classification
# 6. Notification Service

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
