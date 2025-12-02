import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        if not api_key:
            logger.warning("GEMINI_API_KEY not set — Gemini responses will fail.")
        else:
            genai.configure(api_key=api_key)
        self.model_name = model

    def generate_response(self, messages: list) -> str:
        try:
            dialog_text = ""
            for m in messages:
                dialog_text += f"{m['role'].upper()}: {m['content']}\n\n"

            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(dialog_text)

            if hasattr(response, "text"):
                return response.text.strip()

            return "Sorry, I couldn't generate a response."

        except Exception as e:
            logger.exception("Gemini API error: %s", e)
            return "Sorry, I encountered an error while trying to answer."