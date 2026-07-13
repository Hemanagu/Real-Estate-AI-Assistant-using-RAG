from typing import List, Tuple
from langchain_core.documents import Document
from rag.vector_store import QdrantVectorStoreManager
from utils.helpers import logger


class RealEstateRetriever:
    """Manages document retrieval from the local Qdrant vector store."""

    def __init__(self, vector_store_manager: QdrantVectorStoreManager):
        self.manager = vector_store_manager

    def retrieve(self, query: str, k: int = 10) -> List[Document]:
        """Retrieve documents using MMR search."""

        vector_store = self.manager.get_vector_store()

        if not vector_store:
            logger.warning("Vector store is not initialized.")
            return []

        try:
            retriever = vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": k,
                    "fetch_k": 20,
                    "lambda_mult": 0.5
                }
            )

            docs = retriever.invoke(query)

            logger.info(f"Retrieved {len(docs)} documents.")

            return docs

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []

    def retrieve_with_scores(self, query: str, k: int =10)-> List[Tuple[Document, float]]:
        """Retrieve documents with similarity scores."""

        vector_store = self.manager.get_vector_store()

        if not vector_store:
            return []

        try:
            return vector_store.similarity_search_with_score(query, k=k)

        except Exception as e:
            logger.error(f"Retrieval with scores failed: {e}")
            return []