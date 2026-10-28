from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

db_path = os.getenv("DB_PATH")

engine = create_engine(
    db_path,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)