from flask import Blueprint, request, Response, url_for
import logging
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.ai_service import AIService
from app.services.pdf_service import PDFService
from app.services.voice_service import VoiceService
from app.models.conversation import ConversationStore
from app.config import config
from app.services.web_scraper import WebScraper

logger = logging.getLogger(__name__)
voice_bp = Blueprint('voice', __name__)

conversation_store = ConversationStore()

try:
    pdf_service = PDFService(config.PDF_PATH)
    pdf_text = pdf_service.extract_text()[:15000]
    web_scraper = WebScraper()

    # Scraping website content
    web_content = ""
    try:
        if hasattr(config, 'WEBSITE_URLS') and config.WEBSITE_URLS:
            web_content = web_scraper.scrape_multiple_urls(config.WEBSITE_URLS)
            logger.info(f"Successfully scraped {len(web_content)} characters from websites")
        else:
            web_content = "No website URLs configured. Using PDF content only."
            logger.warning("No WEBSITE_URLS configured in config")
    except Exception as e:
        web_content = f"Could not retrieve web content: {str(e)}"
        logger.error(f"Web scraping failed: {e}")

    SYSTEM_PROMPT = (
        "You are a Student Assistant AI for Metropolia University. Use the information below "
        "from both the PDF manual and official websites to answer questions accurately. "
        "If the answer is not found in the provided information, politely say so and suggest "
        "checking the official Metropolia website.\n\n"
        "PDF MANUAL CONTENT:\n"
        f"{pdf_text}\n\n"
        "WEBSITE CONTENT:\n"
        f"{web_content}\n\n"
        "Keep voice responses concise, natural for speech, and helpful."
    )

    ai_service = AIService(config.GEMINI_API_KEY, config.GEMINI_MODEL)
    voice_service = VoiceService(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN, config.TWILIO_PHONE_NUMBER)
    logger.info("All services initialized successfully")

except Exception as e:
    logger.error(f"Service initialization failed: {e}")
    SYSTEM_PROMPT = "You are a Student Assistant AI for Metropolia University. Answer questions helpfully."
    ai_service = None
    web_scraper = None
    voice_service = None

def build_messages(session_id: str):
    try:
        history = conversation_store.get_messages(session_id)
        return [{"role": "system", "content": SYSTEM_PROMPT}] + history
    except Exception as e:
        logger.error(f"Error building messages for session {session_id}: {e}")
        return [{"role": "system", "content": SYSTEM_PROMPT}]


def create_fallback_voice_response(prompt="Please ask your question."):
    resp = VoiceResponse()
    resp.say(prompt, voice='alice')
    gather = Gather(
        input='speech',
        action=url_for('voice.process_speech'),
        method='POST',
        speech_timeout=5,
        speech_model='phone_call',
        language='en-US'
    )
    gather.say("What else can I help with?")
    resp.append(gather)
    resp.say("Thank you for calling. Goodbye!")
    resp.hangup()
    return str(resp)


# Routes
@voice_bp.route("/voice", methods=["GET","POST"])
def voice():
    try:
        session_id = request.form.get("CallSid", f"voice_{request.remote_addr}")
        if not conversation_store.session_exists(session_id):
            conversation_store.create_session(session_id)

        resp = VoiceResponse()
        if request.method == "GET":
            resp.say("Metropolia Student Assistant is ready for your call!")
            return Response(str(resp), mimetype='text/xml')

        if voice_service:
            try:
                twiml_response = voice_service.create_voice_response()
            except Exception as e:
                logger.error(f"VoiceService error: {e}")
                twiml_response = create_fallback_voice_response()
        else:
            twiml_response = create_fallback_voice_response()

        return Response(twiml_response, mimetype='text/xml')

    except Exception as e:
        logger.error(f"Error in /voice endpoint: {e}")
        return Response(create_fallback_voice_response(), mimetype='text/xml')


@voice_bp.route("/test-voice", methods=["GET", "POST"])
def test_voice():
    resp = VoiceResponse()
    resp.say("Hello! This is a test from Metropolia Student Assistant.")
    resp.say("If you can hear this, your voice system is working!")
    resp.hangup()
    return Response(str(resp), mimetype='text/xml')


@voice_bp.route("/process_speech", methods=["POST"])
def process_speech():
    try:
        session_id = request.form.get("CallSid", f"voice_{request.remote_addr}")
        speech_result = request.form.get("SpeechResult", "").strip()
        logger.info(f"Processing speech: '{speech_result}' for session: {session_id}")

        if not speech_result:
            return Response(create_fallback_voice_response("I didn't hear anything. Please try again."),
                            mimetype='text/xml')

        conversation_store.add_message(session_id, "user", speech_result)

        ai_text = "I'm currently having trouble accessing information. Please try again later."
        if ai_service:
            try:
                messages = build_messages(session_id)
                ai_text = ai_service.generate_response(messages)
                logger.info(f"AI generated response: {ai_text[:100]}...")
            except Exception as e:
                logger.error(f"AIService error: {e}")

        # Clean response for voice
        ai_text = ai_text.strip()
        ai_text = ai_text.replace('**', '').replace('*', '')
        if len(ai_text) > 500:
            ai_text = ai_text[:497] + "..."

        conversation_store.add_message(session_id, "assistant", ai_text)

        if voice_service:
            try:
                twiml_response = voice_service.create_voice_response(speech_result, ai_text)
            except Exception as e:
                logger.error(f"VoiceService error: {e}")
                twiml_response = create_fallback_voice_response(ai_text)
        else:
            twiml_response = create_fallback_voice_response(ai_text)

        return Response(twiml_response, mimetype='text/xml')

    except Exception as e:
        logger.error(f"Error in process_speech: {e}")
        return Response(create_fallback_voice_response("Sorry, I encountered an error. Please try again."),
                        mimetype='text/xml')


@voice_bp.route("/voice/status", methods=["POST"])
def voice_status():
    try:
        call_status = request.form.get('CallStatus')
        session_id = request.form.get('CallSid')
        logger.info(f"Call status: {call_status} for session: {session_id}")

        if call_status in ('completed', 'failed', 'busy', 'no-answer'):
            if session_id and conversation_store.session_exists(session_id):
                conversation_store.end_session(session_id)
                logger.info(f"Cleaned up voice session: {session_id}")

        return '', 200

    except Exception as e:
        logger.error(f"Error in voice_status: {e}")
        return '', 500


# Update website URLs dynamically
@voice_bp.route("/voice/update-websites", methods=["POST"])
def update_websites():
    try:
        data = request.get_json()
        if not data or 'urls' not in data:
            return {"error": "No URLs provided"}, 400

        global SYSTEM_PROMPT
        web_content = web_scraper.scrape_multiple_urls(data['urls'])
        SYSTEM_PROMPT = (
            "You are a Student Assistant AI for Metropolia University. Use the information below "
            "from both the PDF manual and official websites to answer questions accurately.\n\n"
            "PDF MANUAL CONTENT:\n"
            f"{pdf_text}\n\n"
            "WEBSITE CONTENT:\n"
            f"{web_content}\n\n"
            "Keep voice responses concise and helpful."
        )

        return {
            "message": f"Updated with {len(data['urls'])} URLs",
            "content_length": len(web_content),
            "urls": data['urls']
        }
    except Exception as e:
        logger.error(f"Error updating websites: {e}")
        return {"error": str(e)}, 500