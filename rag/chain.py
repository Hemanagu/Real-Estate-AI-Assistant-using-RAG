from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from rag.retriever import RealEstateRetriever
from rag.memory import ConversationMemoryManager
from utils.helpers import logger


REPHRASE_PROMPT = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""
Given the following conversation history and a follow-up question, rephrase the follow-up question into a standalone question.

Do NOT answer the question.

Chat History:
{chat_history}

Follow-up Question:
{question}

Standalone Question:
"""
)


QA_PROMPT = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template="""
You are an expert Real Estate AI Assistant.

Answer ONLY using the retrieved context.

Instructions:
- Read ALL retrieved context carefully.
- The answer may be spread across multiple retrieved chunks.
- Combine information from multiple chunks whenever necessary.
- Do not ignore relevant information.
- Never invent facts.
- If the answer is not available in the retrieved context, reply:

"I'm sorry, but that information is not available in the knowledge base."

Retrieved Context:
{context}

Conversation History:
{chat_history}

Question:
{question}

Answer:
"""
)


class RAGChain:
    """Conversational RAG Pipeline."""

    def __init__(self, retriever: RealEstateRetriever, llm):
        self.retriever = retriever
        self.llm = llm

    def condense_question(
        self,
        memory: ConversationMemoryManager,
        question: str,
    ) -> str:
        """Convert follow-up questions into standalone questions."""

        history = memory.get_history_as_string()

        if not history:
            return question

        logger.info("Condensing follow-up question...")

        prompt = REPHRASE_PROMPT.format(
            chat_history=history,
            question=question,
        )

        try:
            response = self.llm.invoke(prompt)
            standalone = response.content.strip()

            logger.info(f"Standalone question: {standalone}")

            return standalone

        except Exception as e:
            logger.error(f"Question condensation failed: {e}")
            return question

    def run(
        self,
        memory: ConversationMemoryManager,
        question: str,
    ) -> Tuple[str, List[Document]]:

        logger.info(f"Running RAG for: {question}")

        # Step 1: Rewrite follow-up question if needed
        history = memory.get_history_as_string()

        if history:
            standalone_question = self.condense_question(memory, question)
        else:
            standalone_question = question

        # Step 2: Retrieve documents
        retrieved_docs = self.retriever.retrieve(
            standalone_question,
            k=10,
        )

        # Step 3: Build context
        context = ""

        for i, doc in enumerate(retrieved_docs):

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", 1)

            logger.info(f"Chunk {i+1} | {source} | Page {page}")
            logger.info(doc.page_content[:300])

            context += (
                f"[Source {i+1}: {source} (Page {page})]\n"
                f"{doc.page_content}\n\n"
            )

        if not context.strip():
            context = "No relevant context found in the knowledge base."

        # Step 4: Generate answer

        prompt = QA_PROMPT.format(
            context=context,
            chat_history=history if history else "No prior history.",
            question=standalone_question,
        )

        try:

            logger.info("Generating response from Groq...")

            response = self.llm.invoke(prompt)

            answer = response.content.strip()

            memory.add_user_message(question)
            memory.add_ai_message(answer)

            return answer, retrieved_docs

        except Exception as e:

            logger.error(f"Error generating answer: {e}")

            return (
                f"An error occurred while generating the response: {e}",
                [],
            )