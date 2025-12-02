import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def build_messages(system_prompt: str, conversation_history: list) -> list:
    return [{"role": "system", "content": system_prompt}] + conversation_history

def get_system_prompt(pdf_context: str) -> str:
    return (
        "You are a Student Assistant AI for Metropolia University. "
        "Use the manual below when answering questions. "
        "If the answer is not found, politely say so. "
        "Keep voice responses concise.\n\n"
        f"Manual Content:\n{pdf_context}"
    )
