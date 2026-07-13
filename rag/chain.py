from typing import Any, Dict, List, Tuple
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from rag.retriever import RealEstateRetriever
from rag.memory import ConversationMemoryManager
from utils.helpers import logger

REPHRASE_PROMPT = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""Given the following conversation history and a follow-up question, rephrase the follow-up question to be a standalone question, in its original language, that can be used to search a vector database.
Do NOT answer the question. Just rephrase it if needed, or return it as-is.

Chat History:
{chat_history}

Follow-up Question: {question}
Standalone Question:"""
)

QA_PROMPT = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template="""
You are an expert Real Estate AI Assistant.

You must answer ONLY from the retrieved context.

Instructions:

- Carefully read ALL retrieved context before answering.
- The answer may be spread across multiple retrieved chunks.
- Combine information from multiple chunks whenever necessary.
- Do not ignore relevant information just because it appears later.
- If multiple documents mention the same topic, merge them into one complete answer.
- If the answer is not present anywhere in the retrieved context, say:
"I'm sorry, but that information is not available in the knowledge base."
- Never invent information.

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
    """Combines retrieval, conversation history, LLM, and prompt templates to answer user queries."""

    def __init__(self, retriever: RealEstateRetriever, llm: ChatGoogleGenerativeAI):
        self.retriever = retriever
        self.llm = llm

    def condense_question(self, memory: ConversationMemoryManager, question: str) -> str:
        """Converts user query to a standalone question using conversation history."""
        history_str = memory.get_history_as_string()
        if not history_str:
            return question

        logger.info("Condensing question using conversation history...")
        prompt_text = REPHRASE_PROMPT.format(chat_history=history_str, question=question)
        
        try:
            response = self.llm.invoke(prompt_text)
            standalone = response.content.strip()
            logger.info(f"Rephrased question: '{standalone}'")
            return standalone
        except Exception as e:
            logger.error(f"Error condensing question: {e}")
            return question

    def run(self, memory: ConversationMemoryManager, question: str) -> Tuple[str, List[Document]]:
        """Executes the full conversational RAG pipeline and returns (answer, source_documents)."""
        logger.info(f"Running RAG pipeline for query: '{question}'")
        
        # 1. Condense the query based on conversation history
        history_str = memory.get_history_as_string()
        if history_str:
            standalone_question = self.condense_question(memory, question)
        else:
            standalone_question = question
        
        # 2. Retrieve top 4 relevant chunks
        retrieved_docs = self.retriever.retrieve(standalone_question, k=10)
        
        # 3. Format retrieved documents as context string
        context_str = ""
        for i, doc in enumerate(retrieved_docs):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", 1)
            logger.info(f"Chunk {i+1} | {source} | Page {page}")
            logger.info(doc.page_content[:300])
            context_str += (
        f"[Source {i+1}: {source} (Page {page})]\n"
        f"{doc.page_content}\n\n"
    )
            if not context_str.strip():
                context_str = "No relevant context found in the knowledge base."

        # 4. Generate final answer from LLM
        history_str = memory.get_history_as_string()
        qa_prompt_text = QA_PROMPT.format(
            context=context_str,
            chat_history=history_str if history_str else "No prior history.",
            question=standalone_question
        )
        
        try:
            logger.info("Generating response from Groq LLM..")
            response = self.llm.invoke(qa_prompt_text)
            answer = response.content.strip()
            
            # Save the interaction to memory
            memory.add_user_message(question)
            memory.add_ai_message(answer)
            
            return answer, retrieved_docs
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"An error occurred while generating the response: {str(e)}", []
