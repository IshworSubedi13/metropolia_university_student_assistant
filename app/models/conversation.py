class ConversationStore:
    def __init__(self):
        self.conversations = {}

    def create_session(self, session_id: str):
        self.conversations[session_id] = []

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.conversations:
            self.create_session(session_id)
        self.conversations[session_id].append({"role": role, "content": content})

    def get_messages(self, session_id: str):
        return self.conversations.get(session_id, [])

    def end_session(self, session_id: str):
        if session_id in self.conversations:
            del self.conversations[session_id]
            return True
        return False

    def session_exists(self, session_id: str):
        return session_id in self.conversations

    def setdefault(self, session_id: str):
        if session_id not in self.conversations:
            self.create_session(session_id)