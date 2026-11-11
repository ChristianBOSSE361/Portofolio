#!/usr/bin/env python3
import os
from typing import List

from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# Model stored INSIDE the project -> kept by Render between build and runtime
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models_cache")


class LocalEmbeddings(Embeddings):
    """Computes embeddings locally (ONNX, no PyTorch, no API call)."""

    def __init__(self):
        self.model = TextEmbedding(model_name=MODEL_NAME, cache_dir=CACHE_DIR)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [vector.tolist() for vector in self.model.embed(texts)]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


# `python embeddings.py` -> only downloads the model (used in the build)
if __name__ == "__main__":
    LocalEmbeddings()
    print("==> Embedding model ready in", CACHE_DIR)