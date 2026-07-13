import os
from rag.vector_store import QdrantVectorStoreManager
from rag.retriever import RealEstateRetriever
from utils.helpers import load_environment

def test():
    load_environment()
    db_manager = QdrantVectorStoreManager()
    retriever = RealEstateRetriever(db_manager)
    
    query = "payment plan Skyline Horizon Developers"
    print(f"Testing retrieval for query: '{query}'")
    results = retriever.retrieve_with_scores(query, k=4)
    
    if not results:
        print("No results found!")
        return
        
    for i, (doc, score) in enumerate(results):
        print(f"\nMatch {i+1} (Score: {score:.4f}):")
        print(f"Source: {doc.metadata.get('source')} | Page: {doc.metadata.get('page')}")
        print(f"Content: {doc.page_content[:150]}...")

if __name__ == "__main__":
    test()
