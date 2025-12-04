# Metropolia University Student Assistant

## Project Overview

The **Metropolia University Student Assistant** is a voice- and text-enabled AI system built using **Flask**, **Gemini LLM**, and real-time telephony/web interfaces. It acts as a 24/7 automated support system capable of answering student queries, guiding visitors, and providing official university information.

Its purpose is to modernize the university’s communication channels by integrating an LLM-powered backend with structured knowledge extracted from Metropolia’s official PDFs and website content.

---

### Purpose of the Project

This project was created to:

* Improve the **availability** of student support services.
* Reduce the workload on university staff by automating frequently asked questions.
* Provide **instant answers** through natural conversation.
* Offer a modern and efficient communication channel for students.
* Demonstrate how AI systems can integrate with **telephony** and **real-time conversation processing**.
* Showcase the ability to **build knowledge bases using extracted data** from PDFs and scraped website content for accurate AI responses.

---

## How It Works ?

This project uses **Flask** as the central backend service for managing the workflow between telephony input, user messaging, and the Gemini LLM. To enrich the assistant's knowledge, data has been extracted from Metropolia University resources, including:

* **PDF documents** (using PDF text extraction)
* **Official website pages** (via custom web scraping)

The extracted data forms a dedicated knowledge base that the assistant uses to generate relevant and university-specific answers.

### System Workflow

1. **Incoming Phone Call:** A caller dials the university's dedicated hotline. (Currently using a trial version of Twilio; to test responses, use endpoint POST `/voice`.)
2. **Call Handling System:** The call is answered autonomously using a telephony API (i.e., Twilio).
3. **Audio Streaming:** The caller's voice is streamed in real time to the Gemini model.
4. **Gemini Response:** Gemini analyzes the speech, generates a natural-language response, and sends it back as synthesized voice.
5. **Continuous Conversation:** A fully interactive dialogue continues until the caller's request is completed.

---

### Features

* Real-time voice input and output
* Natural, human-like AI responses
* Handles common university queries (admissions, fees, deadlines, campus info, etc.)
* Works 24/7 without human supervision
* Expandable knowledge base
* Customizable conversation flow

---

### Future Improvements

This project can be expanded in many ways:

* **Student Information System Integration** (grades, schedules, enrollment status)
* **Authentication by student ID, database lookup, or voice recognition**
* **Verification of current student status** through university records
* **Automated certificate generation** (e.g., student certificate, enrollment certificate, attendance certificate)
* **AI-assisted document requests and processing**
* **Smart appointment booking** with faculty/staff
* **Messaging/Chat interface for text-based queries**
* **Multi-language support**
* **WhatsApp, Telegram, and web chat integration**
* **Voice-to-email ticket creation** for unresolved issues

---

## Setup Environment Variables

Create a `.env` file at the root of your project with the following content:

```dotenv
# OpenAI / Gemini configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Twilio configuration (for real phone calls)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_APP_SID=your_twilio_app_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+18782187579

# Knowledge base sources
PDF_PATH=files/metropolia_manual.pdf
WEBSITE_URLS=https://www.metropolia.fi/en,https://www.metropolia.fi/en/apply,https://www.metropolia.fi/en/academics

# Flask server configuration
PORT=3000
```

**Notes:**

* Keep the `.env` file private.
* `WEBSITE_URLS` can store multiple URLs, separated by commas.
* `PORT` defines the Flask server port for local development.

In your `app.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
PDF_PATH = os.getenv("PDF_PATH")
WEBSITE_URLS = os.getenv("WEBSITE_URLS").split(",")
PORT = int(os.getenv("PORT", 3000))
```

---

## How to Use

### Running Locally

1. **Clone the repository:**

```bash
git clone <your_repo_url>
cd project_folder
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Load environment variables:**

```bash
source .env
```

4. **Start the Flask server:**

```bash
python app.py
```

5. Connect your telephony provider or chat interface to the exposed endpoints.

---

### API Endpoints

**Voice Module:**

* `POST /voice` — Handles incoming phone calls
* `POST /process_speech` — Processes speech input and returns AI responses
* `POST /voice/update-websites` — Update knowledge base from new URLs
* `GET /test-voice` — Test voice endpoint
* `POST /voice/status` — Updates call status

**Chat Module:**

* `POST /chat` — Sends user messages and receives AI responses
* `GET /conversation/<session_id>` — Retrieve conversation history
* `DELETE /conversation/<session_id>` — Clear conversation history
* `POST /update-websites` — Update chat knowledge base

**Call Session Module:**

* `POST /start_call` — Start a new call session
* `POST /end_call` — End an existing call session

---

### Requirements

```text
Flask==3.1.2
twilio==9.8.7
google-generativeai==0.8.5
pypdf==6.4.0
beautifulsoup4==4.14.2
requests==2.32.5
lxml==5.1.0
python-dotenv==1.1.1
typing_extensions==4.15.0
```

---

### License

You may adapt or modify this project freely for educational or development use.

---

### Contact

For questions or collaboration, please reach out through email ([ishworsubedi13@gmail.com](mailto:ishworsubedi13@gmail.com)) or website ([https://www.ishworsubedi.com.np](https://www.ishworsubedi.com.np)).
