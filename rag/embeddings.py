from functools import lru_cache

import torch
from langchain_huggingface import HuggingFaceEmbeddings

from utils.helpers import logger


@lru_cache(maxsize=1)
def get_embeddings_model():

    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    device = "cuda" if torch.cuda.is_available() else "cpu"

    logger.info(f"Loading embedding model ({model_name}) on {device}")

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={
            "device": device
        },
        encode_kwargs={
            "normalize_embeddings": True
        },
    )