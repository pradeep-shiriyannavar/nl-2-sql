from app.core.llm_client import call_llm_system

def intent_agent(user_question: str) -> str:
    system = "You are a database intent classifier. Classify the user's natural language question into one of: SELECT, AGGREGATION, INSERT, UPDATE, DELETE, DDL, OTHER. Reply only with the intent token."
    prompt = f"Question: {user_question}\n\nReturn only the single token intent." 
    # print("\n📤 INPUT SENT TO LLM (INTENT AGENT)")
    # print("--------------------------------------------------")
    # print("SYSTEM PROMPT:\n", system)
    # print("\nUSER PROMPT:\n", prompt)
    # print("--------------------------------------------------\n")

    out = call_llm_system(prompt, system=system)
    # sanitize
    token = out.split()[0].upper()
    return token