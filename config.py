from openai import AzureOpenAI
import os

os.getenv

METADATA_STORE = "/app/querygpt_faiss.index"
FAISS_INDEX_PATH = "/app/schema_metadata.json"

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "admin",
    "database": "db_blockchain_ehr_test"
}

AZURE_EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3
MAX_TOKEN = 512

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

