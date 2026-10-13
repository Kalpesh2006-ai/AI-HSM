import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# AI model configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Project paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

GOVERNMENT_SCHEMES_PATH = os.path.join(
    PROJECT_ROOT,
    "rag",
    "government_schemes"
)

QUESTIONS_PATH = os.path.join(
    GOVERNMENT_SCHEMES_PATH,
    "questions",
    "government_scheme_questions.json"
)

DOCUMENTS_PATH = os.path.join(
    GOVERNMENT_SCHEMES_PATH,
    "documents"
)

VECTOR_DB_PATH = os.path.join(
    GOVERNMENT_SCHEMES_PATH,
    "vector_db"
)

# Collection name for ChromaDB
COLLECTION_NAME = "government_schemes"