from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_PATH

print(f"DB_PATH = {repr(DB_PATH)}")

engine = create_engine(
    DB_PATH,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)