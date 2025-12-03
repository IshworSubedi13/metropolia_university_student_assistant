from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import logging

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self, account_sid: str, auth_token: str, phone_number: str):
        self.phone_number = phone_number
        self.client = None

        if account_sid and auth_token:
            try:
                self.client = Client(account_sid, auth_token)
                logger.info("Twilio client initialized successfully")
            except Exception as e:
                logger.warning(f"Unable to initialize Twilio client: {e}")
        else:
            logger.warning("Twilio credentials not provided - voice calls will not work")

    def create_voice_response(self, speech_result: str = None, ai_response: str = None) -> str:
        resp = VoiceResponse()

        try:
            if not speech_result:
                resp.say(
                    "Hello! Welcome to the Metropolia Student Assistant. "
                    "I can help you with course information, deadlines, and university services. "
                    "Please ask your question after the beep.",
                    voice='alice',
                    language='en-US'
                )

                gather = Gather(
                    input='speech',
                    action='/process_speech',
                    method='POST',
                    speech_timeout=3,
                    speech_model='phone_call',
                    language='en-US',
                    enhanced='true'
                )
                gather.say("Please speak now.", voice='alice')
                resp.append(gather)

                resp.say(
                    "We didn't hear your question. Please call back and try again. Goodbye!",
                    voice='alice'
                )
                resp.hangup()
            else:
                if ai_response:
                    resp.say(ai_response, voice='alice', language='en-US')

                gather = Gather(
                    input='speech',
                    action='/process_speech',
                    method='POST',
                    speech_timeout=3,
                    speech_model='phone_call',
                    language='en-US',
                    enhanced='true'
                )
                gather.say(
                    "Do you have another question? Please speak now, or hang up to end the call.",
                    voice='alice'
                )
                resp.append(gather)

                resp.say(
                    "Thank you for calling the Metropolia Student Assistant. Have a great day!",
                    voice='alice'
                )
                resp.hangup()

        except Exception as e:
            logger.error(f"Error creating voice response: {e}")
            resp.say(
                "We're experiencing technical difficulties. Please try again later.",
                voice='alice'
            )
            resp.hangup()

        return str(resp)
