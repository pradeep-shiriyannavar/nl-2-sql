from typing import List,Tuple
from app.core.embedder import Embedder
import faiss
import json
from app.core.schema_extractor import extract_schema_text
import os
from config import FAISS_INDEX_PATH, METADATA_STORE


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

def setup_index_and_metadata(conn, embedder: Embedder, force_rebuild: bool = False):
    # extract schema texts
    schema_texts = extract_schema_text(conn)
    #schema_texts = load_schema_from_file("ehr_schema.txt")  # or ehr_schema.txt

    # prepare docs for FAISS: include table name + schema
    docs = []
    table_list = list(schema_texts.keys())
    for t in table_list:
        docs.append(f"TABLE: {t}\n{schema_texts[t]}")

    if force_rebuild or (not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(METADATA_STORE)):
        print("Building FAISS index from schemas...")
        index = build_faiss_index(docs, embedder, index_path=FAISS_INDEX_PATH, metadata_store=METADATA_STORE)
    else:
        print("Loading existing FAISS index and metadata...")
        index, loaded_docs = load_faiss_index(FAISS_INDEX_PATH, METADATA_STORE)
        docs = loaded_docs

    return index, docs, schema_texts