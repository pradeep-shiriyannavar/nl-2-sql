from app.core.llm_client import call_llm_system
import json

def column_prune_agent(user_question: str, tables: List[str], schema_texts: Dict[str,str]) -> Dict[str,List[str]]:
    """Return a dict table -> columns to keep (pruned), using the LLM to pick most relevant columns."""
    system = ("You are an assistant that, given a question and schemas for chosen tables, returns a JSON mapping of table_name -> [col1, col2,...] containing only the columns necessary to answer the question."
    )
    snippet = "\n\n".join([f"{t}: {schema_texts[t]}" for t in tables])
    prompt = (
        f"Question: {user_question}\n\nSchemas:\n{snippet}\n\n"
        "Return a JSON object mapping table names to a list of column names to keep. Example: {\"m_user\": [\"id\", \"name\"]}"
    )
    
    # print("\n📤 INPUT SENT TO LLM (COLUMN PRUNE AGENT)")
    # print("--------------------------------------------------")
    # print("SYSTEM PROMPT:\n", system)
    # print("\nUSER PROMPT:\n", prompt)
    # print("--------------------------------------------------\n")
    
    out = call_llm_system(prompt, system=system)

    try:
        mapping = json.loads(out)
        # ensure lists
        final = {t: mapping.get(t, []) for t in tables}
        return final
    except Exception:
        # fallback: keep all columns
        final = {}
        for t in tables:
            cols = [line.split()[0] for line in schema_texts[t].split('\n')[1:]]
            final[t] = cols
        return final