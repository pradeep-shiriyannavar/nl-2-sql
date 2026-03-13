from app.core.llm_client import call_llm_system
from typing import List, Dict, Tuple, Any
import json


def table_agent(user_question: str, table_list: List[str], schema_texts: Dict[str, str]) -> List[str]:
    """Ask LLM to pick relevant tables. Returns a list of table names from table_list."""

    system = (
        "You are a helpful assistant that, given a user question and a list of available "
        "tables, returns the best matching tables as a JSON array of table names. "
        "Only return valid table names present in the list."
    )

    processed_schemas = []
    for t in table_list:
        schema_clean = schema_texts[t].replace("\n", " | ")
        processed_schemas.append(f"{t}: {schema_clean}")

    short_schemas = "\n\n".join(processed_schemas)

    prompt = (
        f"User question: {user_question}\n\n"
        f"Available tables and short schemas:\n{short_schemas}\n\n"
        "Return a JSON array of table names that are most relevant (in descending order). "
        "Example: [\"m_user\", \"m_transaction\"]"
    )
    # print("\n📤 INPUT SENT TO LLM (TABLE AGENT)")
    # print("--------------------------------------------------")
    # print("SYSTEM PROMPT:\n", system)
    # print("\nUSER PROMPT:\n", prompt)
    # print("--------------------------------------------------\n")
    
    out = call_llm_system(prompt, system=system)
    
    try:
        arr = json.loads(out)
        arr = [a for a in arr if a in table_list]
        return arr
    except Exception:
        # fallback: simple substring detection
        picks = [t for t in table_list if t in out]
        return picks
