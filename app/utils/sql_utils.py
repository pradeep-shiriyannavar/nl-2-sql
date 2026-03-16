from typing import Dict, Any
import pandas as pd

def safe_execute_select(conn, sql: str, limit_rows: int = 1000) -> pd.DataFrame:
    """Execute given SQL but only if it is a SELECT. Append/overwrite LIMIT if necessary."""
    sql_strip = sql.strip().lower()
    if not sql_strip.startswith('select'):
        raise ValueError("Only SELECT statements allowed in safe execution mode.")
    # ensure LIMIT
    if 'limit' not in sql_strip:
        sql = sql.rstrip(';') + f" LIMIT {limit_rows};"
    df = pd.read_sql(sql, conn)
    return df


def evaluate_generated_sql(generated_sql: str, conn, example_golden: str = None) -> Dict[str,Any]:
    res = {
        'generated_sql': generated_sql,
        'ran': False,
        'rows_returned': None,
        'error': None,
        'exec_time': None
    }
    try:
        # t0 = time.time()
        df = safe_execute_select(conn, generated_sql)
        # t1 = time.time()
        res['ran'] = True
        res['rows_returned'] = len(df)
        # res['exec_time'] = t1 - t0
        # print(res['exec_time'])
    except Exception as e:
        res['error'] = str(e)
    return res