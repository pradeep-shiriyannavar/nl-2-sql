from config import DB_CONFIG

def extract_schema_text(conn) -> Dict[str, str]:
    """Extract table schemas from INFORMATION_SCHEMA and return a mapping table_name -> textual schema."""
    cur = conn.cursor(dictionary=True)
    q = ("SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, IS_NULLABLE, COLUMN_COMMENT"
         " FROM INFORMATION_SCHEMA.COLUMNS"
         " WHERE TABLE_SCHEMA = %s"
         " ORDER BY TABLE_NAME, ORDINAL_POSITION")
    cur.execute(q, (DB_CONFIG['database'],))
    rows = cur.fetchall()
    cur.close()

    schema_map = {}
    for r in rows:
        t = r['TABLE_NAME']
        entry = f"{r['COLUMN_NAME']} {r['COLUMN_TYPE']} {r['COLUMN_KEY']} nullable:{r['IS_NULLABLE']} comment:{r.get('COLUMN_COMMENT','')}"
        schema_map.setdefault(t, []).append(entry)

    # format into readable blocks
    schema_texts = {}
    for t, cols in schema_map.items():
        schema_texts[t] = f"TABLE: {t}\n" + "\n".join(cols)
    return schema_texts