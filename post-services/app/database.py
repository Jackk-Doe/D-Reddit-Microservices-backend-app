from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import load_envs as _envs

# This one for create SQLite DB only : Sqlite databse URL
# DATABASE_URL = "sqlite:///./post.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Docker test
DATABASE_URL = _envs.DATABASE_URL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
