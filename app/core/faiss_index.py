from typing import List
from app.core.embedder import Embedder
import faiss
import json

def build_faiss_index(docs: List[str], embedder: Embedder, index_path: str = None, metadata_store: str = None):
    # This function converts your text data into a searchable AI memory using numeric vectors.
    embs = embedder.embed_texts(docs)
    import numpy as np
    vecs = np.array(embs).astype('float32')
    embedding_dim = len(embs[0])
    index = faiss.IndexFlatL2(embedding_dim)

    index.add(vecs)
    if index_path:
        faiss.write_index(index, index_path)
    if metadata_store:
        # store docs and metadata
        with open(metadata_store, 'w', encoding='utf-8') as f:
            json.dump({'docs': docs}, f, ensure_ascii=False, indent=2)
    return index


def load_faiss_index(index_path: str, metadata_store: str):
    # Loads the previously saved AI memory back into your program.
    if faiss is None:
        raise RuntimeError("faiss not installed.")
    index = faiss.read_index(index_path)
    with open(metadata_store, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    docs = meta['docs']
    return index, docs


def semantic_search(query: str, index, docs: List[str], embedder: Embedder, k: int = 5) -> List[Tuple[int, float, str]]:
    # Finds most relevant schemas/tables for a user question using meaning, not keywords.
    q_emb = embedder.embed_texts([query])[0]
    import numpy as np
    qv = np.array([q_emb]).astype('float32')
    D, I = index.search(qv, k)
    results = []
    for idx, dist in zip(I[0], D[0]):
        if idx < 0 or idx >= len(docs):
            continue
        results.append((idx, float(dist), docs[idx]))
    return results