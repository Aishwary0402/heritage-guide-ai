import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------
# API KEYS
# -------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# -------------------------
# MODEL SETTINGS
# -------------------------

GEMINI_MODEL = "gemini-2.5-flash-lite"
GROK_MODEL = "llama-3.1-8b-instant"

# -------------------------
# VECTOR DATABASE
# -------------------------

VECTOR_DB_DIR = "vector_db"

# -------------------------
# RAG SETTINGS
# -------------------------

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150