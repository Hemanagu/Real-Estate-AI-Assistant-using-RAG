import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("RealEstateRAG")

def load_environment() -> None:
    """Loads environment variables from .env file."""
    project_dir = Path(__file__).resolve().parent.parent
    env_path = project_dir / ".env"
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info("Environment variables loaded from .env")
    else:
        load_dotenv()  # Fallback to system env
        logger.warning(".env file not found. Falling back to system environment variables.")

def get_gemini_api_key() -> str:
    """Retrieves and validates Gemini API key."""
    load_environment()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Check standard Google API key variable names as well
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in environment or .env file.")
        raise ValueError("GEMINI_API_KEY is missing. Please set it in your environment or .env file.")
    return api_key

def get_qdrant_settings() -> tuple[str, str]:
    """Returns Qdrant path and collection name."""
    load_environment()
    qdrant_path = os.getenv("QDRANT_PATH", "./qdrant_storage")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "real_estate_knowledge")
    return qdrant_path, collection_name

def get_app_credentials() -> tuple[str, str]:
    """Returns app login credentials."""
    load_environment()
    username = os.getenv("APP_USERNAME", "admin")
    password = os.getenv("APP_PASSWORD", "realestate2026")
    return username, password
