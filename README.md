# 🚀 GATE: Gatekeeper and Automated Triage of Emails

## 📌 Table of Contents

- [🚀 GATE: Gatekeeper and Automated Triage of Emails](#-gate-gatekeeper-and-automated-triage-of-emails)
  - [📌 Table of Contents](#-table-of-contents)
  - [🎯 Introduction](#-introduction)
  - [🎥 Demo](#-demo)
  - [💡 Inspiration](#-inspiration)
  - [⚙️ What It Does](#️-what-it-does)
  - [🛠️ How We Built It](#️-how-we-built-it)
  - [🚧 Challenges We Faced](#-challenges-we-faced)
  - [🏃 How to Run](#-how-to-run)
      - [**Prerequisites**](#prerequisites)
    - [**📥 Clone the Repository**](#-clone-the-repository)
    - [**🔧 Setup \& Run the Application**](#-setup--run-the-application)
    - [**📤 Import the Workflow**](#-import-the-workflow)
    - [**🛠 Making Changes \& Keeping Workflows Updated**](#-making-changes--keeping-workflows-updated)
  - [🏗️ Tech Stack](#️-tech-stack)
  - [👥 Team](#-team)

---

## 🎯 Introduction

GATE is a modular email processing pipeline designed to automate workflows using **n8n** and manage data persistence with **MongoDB**. It processes incoming emails, extracts relevant information, classifies them, and sends notifications to appropriate teams. This project aims to streamline email-based workflows for businesses.

## 🎥 Demo

📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration

The project was inspired by the need to automate repetitive email-based workflows, such as processing payment requests, and managing email classification and subsequent notifications to concerned teams.

## ⚙️ What It Does

- Ingests emails via IMAP.
- Parses email body and attachments.
- Extracts structured data from email bodies and attachments.
- Classifies emails into categories using machine learning (BERT based models such as DeBERTa, bart, and modernBERT).
- Detects duplicate or near-duplicate emails.
- Sends notifications to relevant teams based on classification.

## 🛠️ How We Built It

- **Backend**: FastAPI for API endpoints and email processing logic.
- **Database**: MongoDB for storing email metadata and hashes.
- **Workflow Automation**: n8n for managing notifications and workflows.
- **NLP Tools**: SpaCy and Levenshtein for text extraction and fuzzy matching.
- **Machine Learning**: BERT-based models for email classification.
- **Configuration Management**: YAML for category and notification mappings/configs.
- **Docker**: For containerization and deployment.

## 🚧 Challenges We Faced

- Implementing accurate duplicate detection using fuzzy matching.
- Designing a scalable architecture for high email volumes.
- Ensuring seamless integration with n8n workflows and email notifications/ingestions.

## 🏃 How to Run

#### **Prerequisites**  
Make sure you have the following installed before proceeding:  
- **Docker** & **Docker Compose**  
- **Git**  

---

### **📥 Clone the Repository**  
```sh
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

---

### **🔧 Setup & Run the Application**  

1. **Start the application using Docker Compose:**  
   ```sh
   docker-compose up -d
   ```  
2. Open n8n in your browser at:  
   **[http://localhost:5678](http://localhost:5678)**  

---

### **📤 Import the Workflow**  

Since we do not commit the n8n database (`n8n.sqlite`), you need to manually **import the workflow** before using it:  

1. Go to **n8n UI** → Click on **"Import"**  
2. Select the `workflows.json` file from this repo  
3. Click **"Import"** and Save  

> **⚠️ Important:**  
> Make sure to set up any necessary credentials manually in n8n after importing. For example, credentials for IMAP for which inbox to monitor. 

---

### **🛠 Making Changes & Keeping Workflows Updated**  

Whenever you modify workflows, **export and commit them**.

## 🏗️ Tech Stack

- **Backend**: FastAPI  
- **Database**: MongoDB  
- **Workflow Automation**: n8n  
- **NLP Tools**: SpaCy, Levenshtein  
- **Configuration Management**: YAML  
- **Models**: BERT-based models (DeBERTa, bart, modernBERT)

## 👥 Team

- **Anirudh Mishra** - [GitHub](https://github.com/anirudhgray) | [LinkedIn](https://www.linkedin.com/in/anirudh-mishra/)
- **Rohan Khatua** - [GitHub](https://GitHub.com/rohankhatua) | [LinkedIn](https://www.linkedin.com/in/anirudh-mishra)
- **Arnav Chouhan** - [GitHub](https://GitHub.com/arnavnotfound) | [LinkedIn](https://www.linkedin.com/in/arnav-chouhan-450585268/)
- **Param Kansagra** - [GitHub](https://github.com/paramkansagra) | [LinkedIn](https://www.linkedin.com/in/paramkansagra/)
