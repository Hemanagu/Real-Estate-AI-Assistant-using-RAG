from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from utils.helpers import logger


@lru_cache(maxsize=1)
def get_embeddings_model():

    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    logger.info(f"Loading embedding model ({model_name}) on cpu")

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        },
    )