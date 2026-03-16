# tests/test_pipeline.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from app.core.pipeline import run_querygpt_flow


# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def mock_schema_texts():
    return {
        "m_user": "TABLE: m_user\nid INT PRI nullable:NO\nusername VARCHAR(100) nullable:NO\nemail VARCHAR(100) nullable:YES\ncity VARCHAR(100) nullable:YES",
        "m_file_upload": "TABLE: m_file_upload\nf_code INT PRI nullable:NO\nf_name VARCHAR(200) nullable:NO\nowner_id INT MUL nullable:YES",
    }

@pytest.fixture
def mock_conn():
    conn = MagicMock()
    return conn

@pytest.fixture
def mock_embedder():
    embedder = MagicMock()
    embedder.embed_texts.return_value = [[0.1] * 1536]  # fake 1536-dim embedding
    return embedder

@pytest.fixture
def mock_faiss_index():
    index = MagicMock()
    index.d = 1536
    index.ntotal = 2
    # Simulate search returning 2 results
    import numpy as np
    index.search.return_value = (
        np.array([[0.1, 0.2]]),
        np.array([[0, 1]])
    )
    return index

@pytest.fixture
def mock_docs():
    return [
        "TABLE: m_user\nid INT\nusername VARCHAR",
        "TABLE: m_file_upload\nf_code INT\nf_name VARCHAR",
    ]


# ─────────────────────────────────────────────
# UNIT TESTS - AGENTS
# ─────────────────────────────────────────────

class TestIntentAgent:

    @patch("app.agents.intent_agent.call_llm_system", return_value="SELECT")
    def test_select_intent(self, mock_llm):
        from app.agents.intent_agent import intent_agent
        result = intent_agent("How many users are there?")
        assert result == "SELECT"

    @patch("app.agents.intent_agent.call_llm_system", return_value="AGGREGATION")
    def test_aggregation_intent(self, mock_llm):
        from app.agents.intent_agent import intent_agent
        result = intent_agent("Count all users grouped by city")
        assert result == "AGGREGATION"

    @patch("app.agents.intent_agent.call_llm_system", return_value="  select  ")
    def test_intent_uppercased_and_stripped(self, mock_llm):
        from app.agents.intent_agent import intent_agent
        result = intent_agent("show all users")
        assert result == "SELECT"


class TestTableAgent:

    @patch("app.agents.table_agent.call_llm_system", return_value='["m_user"]')
    def test_returns_valid_table(self, mock_llm, mock_schema_texts):
        from app.agents.table_agent import table_agent
        result = table_agent("Show all users", ["m_user", "m_file_upload"], mock_schema_texts)
        assert "m_user" in result

    @patch("app.agents.table_agent.call_llm_system", return_value="invalid json {{")
    def test_fallback_on_bad_json(self, mock_llm, mock_schema_texts):
        from app.agents.table_agent import table_agent
        result = table_agent("Show all users", ["m_user"], mock_schema_texts)
        # fallback: substring match
        assert isinstance(result, list)

    @patch("app.agents.table_agent.call_llm_system", return_value='["nonexistent_table"]')
    def test_filters_invalid_tables(self, mock_llm, mock_schema_texts):
        from app.agents.table_agent import table_agent
        result = table_agent("test", ["m_user"], mock_schema_texts)
        assert "nonexistent_table" not in result


class TestColumnPruneAgent:

    @patch("app.agents.column_prune_agent.call_llm_system",
           return_value='{"m_user": ["id", "username"]}')
    def test_prune_returns_columns(self, mock_llm, mock_schema_texts):
        from app.agents.column_prune_agent import column_prune_agent
        result = column_prune_agent("Show usernames", ["m_user"], mock_schema_texts)
        assert "m_user" in result
        assert "username" in result["m_user"]

    @patch("app.agents.column_prune_agent.call_llm_system", return_value="bad json {{")
    def test_fallback_returns_all_columns(self, mock_llm, mock_schema_texts):
        from app.agents.column_prune_agent import column_prune_agent
        result = column_prune_agent("test", ["m_user"], mock_schema_texts)
        assert "m_user" in result
        assert isinstance(result["m_user"], list)


class TestSQLGenerationAgent:

    @patch("app.agents.sql_generation_agent.call_llm_system",
           return_value="SELECT id, username FROM m_user LIMIT 1000")
    def test_sql_output_is_string(self, mock_llm, mock_schema_texts):
        from app.agents.sql_generation_agent import sql_generation_agent
        sql = sql_generation_agent(
            "Show all users", "SELECT",
            ["m_user"], {"m_user": ["id", "username"]},
            mock_schema_texts
        )
        assert isinstance(sql, str)
        assert sql.strip().endswith(";")

    @patch("app.agents.sql_generation_agent.call_llm_system",
           return_value="```sql\nSELECT * FROM m_user\n```")
    def test_strips_markdown_fences(self, mock_llm, mock_schema_texts):
        from app.agents.sql_generation_agent import sql_generation_agent
        sql = sql_generation_agent(
            "Show all users", "SELECT",
            ["m_user"], {"m_user": ["id"]},
            mock_schema_texts
        )
        assert "```" not in sql
        assert "SELECT" in sql.upper()

    @patch("app.agents.sql_generation_agent.call_llm_system",
           return_value="sql SELECT * FROM m_user LIMIT 1000")
    def test_removes_sql_prefix(self, mock_llm, mock_schema_texts):
        from app.agents.sql_generation_agent import sql_generation_agent
        sql = sql_generation_agent(
            "Show all", "SELECT",
            ["m_user"], {"m_user": ["id"]},
            mock_schema_texts
        )
        assert not sql.strip().lower().startswith("sql ")


# ─────────────────────────────────────────────
# INTEGRATION TEST - FULL PIPELINE
# ─────────────────────────────────────────────

class TestFullPipeline:

    @patch("app.agents.intent_agent.call_llm_system", return_value="SELECT")
    @patch("app.agents.table_agent.call_llm_system", return_value='["m_user"]')
    @patch("app.agents.column_prune_agent.call_llm_system",
           return_value='{"m_user": ["id", "username"]}')
    @patch("app.agents.sql_generation_agent.call_llm_system",
           return_value="SELECT id, username FROM m_user LIMIT 1000")
    @patch("app.utils.sql_utils.pd.read_sql")
    def test_full_pipeline_returns_result(
        self, mock_read_sql,
        mock_sql_gen, mock_col_prune, mock_table, mock_intent,
        mock_conn, mock_embedder, mock_faiss_index, mock_docs, mock_schema_texts
    ):
        import pandas as pd
        mock_read_sql.return_value = pd.DataFrame({"id": [1, 2], "username": ["alice", "bob"]})

        result = run_querygpt_flow(
            user_question="Show all usernames",
            conn=mock_conn,
            embedder=mock_embedder,
            index=mock_faiss_index,
            docs=mock_docs,
            schema_texts=mock_schema_texts
        )

        assert "sql" in result
        assert "result_df" in result
        assert len(result["result_df"]) == 2

    @patch("app.agents.intent_agent.call_llm_system", return_value="SELECT")
    @patch("app.agents.table_agent.call_llm_system", return_value='["m_user"]')
    @patch("app.agents.column_prune_agent.call_llm_system",
           return_value='{"m_user": ["id"]}')
    @patch("app.agents.sql_generation_agent.call_llm_system",
           return_value="SELECT id FROM m_user LIMIT 1000")
    @patch("app.utils.sql_utils.pd.read_sql", side_effect=Exception("DB connection error"))
    def test_pipeline_handles_db_error(
        self, mock_read_sql,
        mock_sql_gen, mock_col_prune, mock_table, mock_intent,
        mock_conn, mock_embedder, mock_faiss_index, mock_docs, mock_schema_texts
    ):
        result = run_querygpt_flow(
            user_question="Show all users",
            conn=mock_conn,
            embedder=mock_embedder,
            index=mock_faiss_index,
            docs=mock_docs,
            schema_texts=mock_schema_texts
        )
        # Should return empty df, not crash
        assert result["result_df"].empty