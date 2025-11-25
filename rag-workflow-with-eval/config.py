import os

from dotenv import load_dotenv

load_dotenv()

class RAGConfig:
    # Local RAG configuration
    MODEL_NAME = "llama3.2"
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
    CONTEXT_WINDOW = 4096
    NUM_BATCH = 128

    # API Keys and Hosts
    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    RAGAS_JUDGE_MODEL = os.getenv("RAGAS_JUDGE_MODEL", "gpt-4.1-nano")