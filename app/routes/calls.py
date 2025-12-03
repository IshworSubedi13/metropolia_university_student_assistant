from flask import Blueprint, request, jsonify
import os
import logging
from app.models.conversation import ConversationStore

logger = logging.getLogger(__name__)
calls_bp = Blueprint('calls', __name__)

conversation_store = ConversationStore()

@calls_bp.route("/start_call", methods=["POST"])
def start_call():
    session_id = f"session_{int(os.times()[4])}"
    conversation_store.create_session(session_id)
    logger.info("Started session %s", session_id)
    return jsonify({"message": "Call started.", "session_id": session_id})

@calls_bp.route("/end_call", methods=["POST"])
def end_call():
    session_id = request.json.get("session_id")
    if conversation_store.end_session(session_id):
        return jsonify({"message": "Call ended."})
    return jsonify({"message": "Session not found"}), 404