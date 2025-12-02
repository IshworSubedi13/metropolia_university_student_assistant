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

1. **Incoming Phone Call:** A caller dials the university's dedicated hotline.
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
* **Automated certificate generation** (e.g., enrollment certificate, attendance certificate)
* **AI-assisted document requests and processing**
* **Smart appointment booking** with faculty/staff
* **Messaging/Chat interface for text-based queries**
* **Multi-language support**
* **WhatsApp, Telegram, and web chat integration**
* **Voice-to-email ticket creation** for unresolved issues

---

### License

You may adapt or modify this project freely for educational or development use.

---

### Contact

For questions or collaboration, please reach out through email (ishworsubedi13@gmail.com) or website (https://www.ishworsubedi.com.np).
