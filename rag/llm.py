from langchain_groq import ChatGroq
from utils.helpers import logger
import os
def get_llm():
    try:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing in .env")

        logger.info("Initializing Groq LLM...")

        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.2,
        )

        logger.info("Groq LLM initialized successfully.")

        return llm

    except Exception as e:
        logger.error(f"Error initializing Groq LLM: {e}")
        raise