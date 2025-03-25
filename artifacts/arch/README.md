# **Architecture and Design Documentation**

## **High-Level Overview**

The project is designed as a modular email processing pipeline that integrates with **n8n** for workflow automation and **MongoDB** for data persistence. The system processes incoming emails, extracts relevant information, classifies them, and sends notifications to appropriate teams based on predefined mappings.

![sequence diagram](/artifacts/arch/sequence.png)

---

### **System Components**

1. **Email Ingestion Node**:
   - Handles the ingestion of raw emails from external sources (e.g., IMAP, n8n workflows).
   - Converts raw email data into a structured format for further processing.

2. **Processing Black Box**:
   - The core of the system, responsible for processing emails end-to-end.
   - Composed of the following subcomponents:
     - **Email Ingestion Handler**: Converts raw email data into structured objects.
     - **Email and Attachment Parser**: Extracts text from email bodies and attachments (e.g., PDFs, DOCX).
     - **Email Data Extractor**: Extracts structured fields (e.g., amounts, dates, entities) using NLP tools like SpaCy.
     - **Email Category Classifier**: Classifies emails into predefined categories and subcategories using machine learning models.
     - **Duplicate Checker**: Detects duplicate or near-duplicate emails using fuzzy matching and MongoDB.
     - **Notification Generator**: Maps email categories to recipients and sends notifications via n8n.

3. **Email Notification Node**:
   - Sends notifications to relevant teams based on the classification and extracted data.
   - Uses n8n workflows to handle notification delivery.

---

### **Data Flow**

1. **Input**:
   - Emails are ingested via the `/process-email` API endpoint.
   - Example payload:
     ```json
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

2. **Processing**:
   - **Duplicate Detection**:
     - Checks for duplicates using a hash of normalized email content.
     - Uses fuzzy matching for near-duplicate detection.
   - **Parsing**:
     - Extracts text from email bodies and attachments.
   - **Data Extraction**:
     - Extracts structured fields like amounts, dates, and entities using SpaCy.
   - **Classification**:
     - Classifies emails into categories and subcategories using machine learning models.
   - **Notification Mapping**:
     - Maps categories to recipient email addresses using a YAML configuration file.

3. **Output**:
   - Sends notifications to relevant teams via n8n.
   - Example notification payload:
     ```json
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

---

### **Key Modules**

#### **1. Duplicate Checker**
- **Purpose**: Detects duplicate or near-duplicate emails.
- **Implementation**:
  - Uses MongoDB to store email hashes and metadata.
  - Performs fuzzy matching on email `subject` and `body` using `Levenshtein`.
- **Key Functions**:
  - `generate_email_hash`: Generates a hash of normalized email content.
  - `is_duplicate`: Checks for duplicates in the MongoDB `emails` collection.

#### **2. Email Classifier**
- **Purpose**: Classifies emails into predefined categories and subcategories.
- **Implementation**:
  - Loads categories and subcategories from a YAML configuration file.
  - Combines categories and subcategories into labels for classification.
- **Key Functions**:
  - `load_categories_config`: Loads categories and subcategories from `categories_config.yaml`.

#### **3. Notification Service**
- **Purpose**: Sends notifications to relevant teams based on email classification.
- **Implementation**:
  - Maps categories to recipients using `notification_mapper_config.yaml`.
  - Sends notifications via n8n using a REST API.
- **Key Functions**:
  - `load_notification_mapping`: Loads the category-to-recipients mapping.
  - `send_notification`: Sends notifications to n8n.

---

### **Configuration Files**

1. **`categories_config.yaml`**:
   - Defines categories and subcategories for email classification.
   - Example:
     ```yaml
     categories:
       - AU Transfer
       - Closing Notice
     subcategories:
       AU Transfer:
         - Reallocation Fees
         - Amendment Fees
     ```

2. **`notification_mapper_config.yaml`**:
   - Maps categories to recipient email addresses.
   - Example:
     ```yaml
     category_to_recipients:
       AU Transfer:
         - au-team@example.com
       Closing Notice:
         - closing-team@example.com
     ```

---

### **Tech Stack**

- **Backend**: FastAPI
- **Database**: MongoDB
- **Workflow Automation**: n8n
- **NLP Tools**: SpaCy, Levenshtein
- **Configuration Management**: YAML

---

### **Deployment**

1. **Docker Compose**:
   - Services:
     - `email_processor`: Handles email processing.
     - `mongo`: Stores email metadata and hashes.
     - `n8n`: Manages workflows and notifications.
   - Example `docker-compose.yml`:
     ```yaml
     services:
       email_processor:
         build: ./code
         container_name: email_processor
         ports:
           - "8000:8000"
         depends_on:
           - mongo
       mongo:
         image: mongo:latest
         container_name: mongo
         ports:
           - "27017:27017"
         volumes:
           - ./mongo_data:/data/db
       n8n:
         image: n8nio/n8n
         container_name: n8n
         ports:
           - "5678:5678"
         depends_on:
           - mongo
           - email_processor
     ```

2. **Environment Variables**:
   - `MONGO_URI`: MongoDB connection string.
   - `NOTIF_ENDPOINT`: n8n endpoint for sending notifications.

---

### **Future Enhancements**

1. **Partial Duplicate Detection**:
   - Improve fuzzy matching by incorporating additional fields like attachments.

2. **Dynamic Notification Mapping**:
   - Allow dynamic updates to `notification_mapper_config.yaml` without restarting the service.

3. **Enhanced Classification**:
   - Use pre-trained models for better classification accuracy.

4. **Scalability**:
   - Add support for distributed processing to handle high email volumes.

---
