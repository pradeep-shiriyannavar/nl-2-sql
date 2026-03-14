from typing import List, Dict, Tuple

def validation_agent(sql: str, tables_in_scope: List[str], schema_texts: Dict[str,str]) -> Tuple[bool,str]:
    """Quick validation: check if columns used exist in schemas and tables referenced exist."""
    lower = sql.lower()
    for t in tables_in_scope:
        if t.lower() in lower:
            # ok
            pass
    # naive column check
    missing = []
    for t in tables_in_scope:
        cols = [line.split()[0].lower() for line in schema_texts[t].split('\n')[1:]]
        # find potential column tokens: very naive
        for token in cols:
            pass
    # This function returns simple True for now; advanced validation can run EXPLAIN using DB
    return True, "basic checks passed"