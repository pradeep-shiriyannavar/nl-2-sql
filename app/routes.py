from flask import Blueprint, request, jsonify, render_template
from app.core.pipeline import run_querygpt_flow
from app.core.embedder import Embedder
from app.core.faiss_index import setup_index_and_metadata
from app.db.connection import get_mysql_connection
from config import DB_CONFIG

main = Blueprint("main", __name__)

# Initialize once at startup
conn       = get_mysql_connection(DB_CONFIG)
embedder   = Embedder()
index, docs, schema_texts = setup_index_and_metadata(conn, embedder, force_rebuild=True)


@main.route("/")
def home():
    return render_template("index.html")

@main.route("/query", methods=["POST"])
def query():
    data     = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question cannot be empty."}), 400

    try:
        result = run_querygpt_flow(
            user_question=question,
            conn=conn,
            embedder=embedder,
            index=index,
            docs=docs,
            schema_texts=schema_texts
        )

        df = result.get("result_df")

        return jsonify({
            "sql":     result.get("sql", ""),
            "intent":  result.get("intent", ""),
            "tables":  result.get("tables", []),
            "columns": result.get("result_df", None).columns.tolist() if df is not None and not df.empty else [],
            "rows":    df.values.tolist() if df is not None and not df.empty else [],
            "count":   len(df) if df is not None else 0
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500