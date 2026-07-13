from typing import Any, Dict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from utils.helpers import logger

class ConversationMemoryManager:
    """Manages multi-turn conversation history for the assistant."""

    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_user_message(self, text: str) -> None:
        """Adds a user message to the memory."""
        self.messages.append({"role": "user", "content": text})

    def add_ai_message(self, text: str) -> None:
        """Adds an AI assistant response to the memory."""
        self.messages.append({"role": "assistant", "content": text})

    def get_messages(self) -> List[Dict[str, str]]:
        """Returns all messages in the history."""
        return self.messages

    def clear(self) -> None:
        """Clears all conversation memory."""
        self.messages = []
        logger.info("Conversation memory cleared.")

    def get_history_as_langchain_messages(self) -> List[BaseMessage]:
        """Converts internal messages into LangChain message objects."""
        lc_messages = []
        for msg in self.messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        return lc_messages

    def get_history_as_string(self) -> str:
        """Formats the history as a dialogue string for standard prompting."""
        formatted = []
        for msg in self.messages:
            role_name = "Human" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role_name}: {msg['content']}")
        return "\n".join(formatted)
