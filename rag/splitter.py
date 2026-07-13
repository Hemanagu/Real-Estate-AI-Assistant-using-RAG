from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.helpers import logger

class DocumentSplitter:
    """Chunks documents into smaller, overlapping segments using RecursiveCharacterTextSplitter."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def split(self, documents: List[Document]) -> List[Document]:
        """Splits a list of documents into chunks and retains metadata."""
        logger.info(f"Splitting {len(documents)} documents with chunk_size={self.chunk_size}, overlap={self.chunk_overlap}")
        chunks = self.splitter.split_documents(documents)
        logger.info(f"Generated {len(chunks)} text chunks.")
        
        # Add a unique chunk ID in metadata to help with trace/debugging if needed
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"{chunk.metadata.get('source', 'unknown')}_chunk_{i}"
            
        return chunks
