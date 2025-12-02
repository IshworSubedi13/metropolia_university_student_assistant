from flask import Blueprint, request, jsonify
import logging
from app.services.ai_service import AIService
from app.services.pdf_service import PDFService
from app.services.web_scraper import WebScraper
from app.models.conversation import ConversationStore
from app.config import config

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__)

try:
    pdf_service = PDFService(config.PDF_PATH)
    web_scraper = WebScraper()

    pdf_text = pdf_service.extract_text()
    if not pdf_text:
        logger.warning("PDF content empty — manual context unavailable.")
        pdf_text = "No PDF content available."

    # Scraping website content
    web_content = ""
    try:
        if hasattr(config, 'WEBSITE_URLS') and config.WEBSITE_URLS:
            web_content = web_scraper.scrape_multiple_urls(config.WEBSITE_URLS)
            logger.info(f"Successfully scraped {len(web_content)} characters from websites")
        else:
            web_content = "No website URLs configured."
            logger.warning("No WEBSITE_URLS configured in config")
    except Exception as e:
        web_content = f"Could not retrieve web content: {str(e)}"
        logger.error(f"Web scraping failed: {e}")

    # Build comprehensive system prompt
    SYSTEM_PROMPT = (
        "You are a Student Assistant AI for Metropolia University. Use the information below "
        "from both the PDF manual and official websites to answer questions accurately. "
        "If the answer is not found in the provided information, politely say so and suggest "
        "checking the official Metropolia website.\n\n"
        "PDF MANUAL CONTENT:\n"
        f"{pdf_text}\n\n"
        "WEBSITE CONTENT:\n"
        f"{web_content}\n\n"
        "Keep responses helpful, accurate, and student-focused."
    )

    ai_service = AIService(config.GEMINI_API_KEY, config.GEMINI_MODEL)
    conversation_store = ConversationStore()

    logger.info("Chat services initialized successfully")
    logger.info(f"PDF content: {len(pdf_text)} characters")
    logger.info(f"Web content: {len(web_content)} characters")

except Exception as e:
    logger.error(f"Chat service initialization failed: {e}")
    SYSTEM_PROMPT = "You are a Student Assistant AI for Metropolia University. Answer questions helpfully."
    ai_service = None
    conversation_store = ConversationStore()


#Building messages with conversation history
def build_messages(session_id: str):
    try:
        history = conversation_store.get_messages(session_id)
        return [{"role": "system", "content": SYSTEM_PROMPT}] + history
    except Exception as ex:
        logger.error(f"Error building messages for session {session_id}: {ex}")
        return [{"role": "system", "content": SYSTEM_PROMPT}]


# Chat endpoint
@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        if len(user_message) > 1000:
            return jsonify({"error": "Message too long (max 1000 characters)"}), 400

        conversation_store.add_message(session_id, "user", user_message)
        messages = build_messages(session_id)

        # Generating AI response
        if ai_service:
            try:
                ai_text = ai_service.generate_response(messages)
            except Exception as ex:
                logger.error(f"AIService error: {ex}")
                ai_text = "Sorry, I'm having trouble generating a response right now. Please try again."
        else:
            ai_text = "AI service is currently unavailable. Please try again later."

        # Adding AI response to conversation
        conversation_store.add_message(session_id, "assistant", ai_text)

        return jsonify({
            "response": ai_text,
            "session_id": session_id
        })

    except Exception as ex:
        logger.error(f"Chat endpoint error: {ex}")
        return jsonify({"error": "Internal server error"}), 500


# Getting conversation history
@chat_bp.route("/conversation/<session_id>", methods=["GET"])
def get_conversation(session_id):
    try:
        messages = conversation_store.get_messages(session_id)
        # Filter out system prompt for frontend display
        user_messages = [msg for msg in messages if msg.get("role") != "system"]
        return jsonify({
            "session_id": session_id,
            "messages": user_messages
        })
    except Exception as ex:
        logger.error(f"Get conversation error: {ex}")
        return jsonify({"error": "Failed to get conversation"}), 500


# Clear conversation
@chat_bp.route("/conversation/<session_id>", methods=["DELETE"])
def clear_conversation(session_id):
    try:
        if conversation_store.end_session(session_id):
            return jsonify({"message": "Conversation cleared"})
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as ex:
        logger.error(f"Clear conversation error: {ex}")
        return jsonify({"error": "Failed to clear conversation"}), 500


# Update website URLs dynamically
@chat_bp.route("/update-websites", methods=["POST"])
def update_websites():
    try:
        data = request.get_json()
        if not data or 'urls' not in data:
            return jsonify({"error": "No URLs provided"}), 400

        global SYSTEM_PROMPT
        website_content = web_scraper.scrape_multiple_urls(data['urls'])
        SYSTEM_PROMPT = (
            "You are a Student Assistant AI for Metropolia University. Use the information below "
            "from both the PDF manual and official websites to answer questions accurately.\n\n"
            "PDF MANUAL CONTENT:\n"
            f"{pdf_text}\n\n"
            "WEBSITE CONTENT:\n"
            f"{website_content}\n\n"
            "Keep responses helpful and accurate."
        )

        return jsonify({
            "message": f"Updated with {len(data['urls'])} URLs",
            "content_length": len(web_content),
            "urls": data['urls']
        })

    except Exception as ex:
        logger.error(f"Error updating websites: {ex}")
        return jsonify({"error": str(e)}), 500
