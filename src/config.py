from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

DB_PATH = os.getenv("DB_PATH")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = BASE_DIR.parent