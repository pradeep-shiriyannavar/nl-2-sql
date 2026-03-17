from app.core.llm_client import call_llm_system
from typing import List, Dict

def sql_generation_agent(user_question: str, intent: str, tables: List[str], pruned_columns: Dict[str,List[str]], schema_texts: Dict[str,str]) -> str:
    system = (
        "You are an expert SQL generator. Use the provided schema snippets and pruned columns. "
        "Produce a single syntactically valid SQL statement that answers the user's question. "
        "Return ONLY raw SQL. Do NOT include 'sql', markdown, or comments."
    )

    schema_ctx = "\n\n".join([
        f"-- {t}\n{schema_texts[t]}\nKept columns: {pruned_columns.get(t, [])}"
        for t in tables
    ])

    prompt = (
        f"User question: {user_question}\n"
        f"Intent: {intent}\n"
        f"Tables in-scope: {tables}\n\n"
        f"{schema_ctx}\n\n"
        "Rules:\n"
        "- Output ONLY executable SQL.\n"
        "- DO NOT prefix with 'sql'.\n"
        "- DO NOT use markdown.\n"
        "- Always include LIMIT 1000.\n"
    )
    
    # print("\n INPUT SENT TO LLM FOR SQL GENERATION:")
    # print("--------------------------------------------------")
    # print(prompt)
    # print("--------------------------------------------------\n")

    out = call_llm_system(prompt, system=system)

    #  HARD SANITIZATION (VERY IMPORTANT)
    out = out.strip()
    out = out.replace("```sql", "").replace("```", "")
    out = out.replace("sql", "", 1).strip()   #  removes `sql` prefix if model adds it
    out = out.rstrip(";") + ";"

    return out