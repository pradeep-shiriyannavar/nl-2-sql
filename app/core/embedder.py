from typing import List
from config import client,AZURE_EMBED_MODEL

class Embedder:
    def __init__(self, model_name: str = AZURE_EMBED_MODEL):
        self.model_name = model_name

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Takes a list of strings → returns list of embeddings.
        Handles batching automatically.
        """
        BATCH_SIZE = 16
        all_embeddings = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i : i + BATCH_SIZE]

            resp = client.embeddings.create(
                model=self.model_name,
                input=batch
            )

            batch_embeddings = [item.embedding for item in resp.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings
