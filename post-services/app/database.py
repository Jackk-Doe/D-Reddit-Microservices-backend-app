from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# This one for create SQLite DB only : Sqlite databse URL
# DATABASE_URL = "sqlite:///./post.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Docker test
DATABASE_URL = "postgresql://root:password@localhost:5432/room-db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
