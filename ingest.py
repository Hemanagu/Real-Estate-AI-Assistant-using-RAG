import os
import argparse
import sys
from pathlib import Path
from utils.helpers import logger, load_environment
from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.vector_store import QdrantVectorStoreManager

def main():
    parser = argparse.ArgumentParser(description="Ingest documents into the local Qdrant vector database.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the existing collection and build index from scratch."
    )
    args = parser.parse_args()

    # Load environments
    load_environment()

    # Define paths
    project_dir = Path(__file__).resolve().parent
    data_dir = project_dir / "data"
    
    if not data_dir.exists():
        logger.error(f"Data folder not found at: {data_dir}. Please ensure it is copied.")
        sys.exit(1)

    logger.info("=== Starting Data Ingestion ===")
    
    # 1. Load documents
    try:
        loader = DocumentLoader(str(data_dir))
        documents = loader.load_all()
        if not documents:
            logger.warning("No documents were found in the data directory.")
            sys.exit(0)
    except Exception as e:
        logger.error(f"Error loading documents: {e}", exc_info=True)
        sys.exit(1)

    # 2. Split documents
    try:
        splitter = DocumentSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split(documents)
    except Exception as e:
        logger.error(f"Error splitting documents: {e}", exc_info=True)
        sys.exit(1)

    # 3. Create vector store and index
    try:
        manager = QdrantVectorStoreManager()
        manager.build_or_update_index(chunks, reset=args.reset)
        logger.info("=== Ingestion Completed Successfully ===")
    except Exception as e:
        logger.error(f"Error indexing chunks in vector store: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
