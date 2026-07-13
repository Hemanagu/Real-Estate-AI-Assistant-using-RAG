import os
from typing import List, Optional

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from rag.embeddings import get_embeddings_model
from utils.helpers import logger, get_qdrant_settings


class QdrantVectorStoreManager:
    """Manages the local Qdrant vector database."""

    def __init__(self):
        self.qdrant_path, self.collection_name = get_qdrant_settings()

        self.client = None
        self.vector_store = None
        self.embeddings = None

        self._init_client()

    def _init_client(self):
        logger.info(f"Connecting to Qdrant at: {self.qdrant_path}")

        if (
            not self.qdrant_path.startswith(":")
            and self.qdrant_path != "inmemory"
        ):
            os.makedirs(self.qdrant_path, exist_ok=True)

        self.client = QdrantClient(path=self.qdrant_path)

    def _get_vector_store(self):
        """Lazy load vector store only when needed."""

        if self.vector_store is None:

            if self.embeddings is None:
                logger.info("Loading embeddings...")
                self.embeddings = get_embeddings_model()

            self.vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=self.collection_name,
                embedding=self.embeddings,
            )

        return self.vector_store

    def build_or_update_index(
        self,
        documents: List[Document],
        reset: bool = False,
    ) -> QdrantVectorStore:

        exists = True

        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            exists = False

        if reset and exists:
            logger.info("Deleting collection...")
            self.client.delete_collection(self.collection_name)
            exists = False

        if not exists:

            logger.info("Creating collection...")

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

        vector_store = self._get_vector_store()

        logger.info(f"Adding {len(documents)} chunks...")

        vector_store.add_documents(documents)

        logger.info("Indexing completed.")

        return vector_store

    def get_vector_store(self):

        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            return None

        return self._get_vector_store()