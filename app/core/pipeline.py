from app.agents.intent_agent import intent_agent
from app.agents.table_agent import table_agent
from app.agents.column_prune_agent import column_prune_agent
from app.agents.sql_generation_agent import sql_generation_agent
from app.agents.validation_agent import validation_agent
from app.utils.sql_utils import evaluate_generated_sql,safe_execute_select
from app.core.faiss_index import semantic_search
from app.core.embedder import Embedder

from typing import Dict
import pandas as pd

def run_querygpt_flow(user_question: str, conn, embedder: Embedder, index, docs, schema_texts: Dict[str,str], allow_writes: bool = False):

    table_list = list(schema_texts.keys())

    print("\n================ QUERYGPT FLOW START ================\n")
    print("🧠 USER QUESTION (TEXT):", user_question)

    # =========================
    # 1️⃣ USER QUESTION → EMBEDDING
    # =========================
    try:
        q_embedding = embedder.embed_texts([user_question])[0]
        print("\n🔢 USER QUESTION EMBEDDING (First 10 values):")
        print(q_embedding[:10])
        print("Embedding Dimension:", len(q_embedding))
    except Exception as e:
        print("⚠️ Embedding failed:", e)
        q_embedding = None

    # =========================
    # 2️⃣ INTENT AGENT
    # =========================
    print('\n=== 🧭 Intent Agent ===')
    try:
        intent = intent_agent(user_question)
    except Exception:
        intent = 'SELECT'
        print('LLM not available for intent agent; defaulting to SELECT')
    print('✅ Intent:', intent)

    # =========================
    # 3️⃣ SEMANTIC SEARCH (FAISS)
    # =========================
    print('\n=== 🔍 Semantic Search (FAISS using embeddings) ===')

    try:
        ss = semantic_search(user_question, index, docs, embedder, k=5)

        print("\n📊 TOP SIMILAR TABLE EMBEDDINGS:")
        for rank, (idx, dist, doc) in enumerate(ss, start=1):
            table_name = doc.split('\n',1)[0].replace('TABLE: ','')
            table_embedding = embedder.embed_texts([doc])[0][:10]

            print(f"\nRank {rank}")
            print("Table:", table_name)
            print("FAISS Distance:", dist)
            print("Table Embedding (First 10 values):")
            print(table_embedding)

        candidates = [docs[idx].split('\n',1)[0].replace('TABLE: ','') for idx,_,_ in ss]

    except Exception as e:
        print("⚠️ Semantic search failed:", e)
        candidates = table_list

    # =========================
    # 4️⃣ TABLE AGENT (LLM)
    # =========================
    print('\n=== 🗂️ Table Agent (LLM Refinement) ===')

    try:
        picks = table_agent(user_question, candidates, schema_texts)
        if not picks:
            picks = candidates[:3]
    except Exception:
        picks = candidates[:3]

    print('✅ Tables selected by LLM:', picks)

    # =========================
    # 5️⃣ COLUMN PRUNE AGENT
    # =========================
    print('\n=== ✂️ Column Prune Agent ===')

    try:
        pruned = column_prune_agent(user_question, picks, schema_texts)
    except Exception:
        pruned = {t: [line.split()[0] for line in schema_texts[t].split('\n')[1:]] for t in picks}

    print('✅ Pruned columns (sample):', {k: pruned[k][:10] for k in pruned})

    # =========================
    # 6️⃣ SQL GENERATION
    # =========================
    print('\n=== 🧮 SQL Generation Agent ===')

    try:
        sql = sql_generation_agent(user_question, intent, picks, pruned, schema_texts)
    except Exception as e:
        raise RuntimeError(f"SQL generation failed: {e}")

    print('✅ Generated SQL:\n', sql)

    # =========================
    # 7️⃣ VALIDATION
    # =========================
    print('\n=== 🛡️ Validation Agent ===')

    ok, msg = validation_agent(sql, picks, schema_texts)
    print('✅ Validation:', ok, msg)

    if not ok:
        return {'error': 'validation_failed', 'message': msg}

    # =========================
    # 8️⃣ EVALUATION (TIME + ROWS)
    # =========================
    eval_result = evaluate_generated_sql(sql, conn)
    print("\n⏱️ Evaluation Result:", eval_result)

    # =========================
    # 9️⃣ SAFE SQL EXECUTION
    # =========================
    print('\n=== ✅ Execute (Safe Mode) ===')

    try:
        df = safe_execute_select(conn, sql)
        print(f"✅ Returned {len(df)} rows.\n")
    except Exception as e:
        print('❌ Execution error:', e)
        df = pd.DataFrame()

    print("\n================ QUERYGPT FLOW END ================\n")

    return {
        'intent': intent,
        'tables': picks,
        'pruned': pruned,
        'sql': sql,
        'result_df': df
    }
