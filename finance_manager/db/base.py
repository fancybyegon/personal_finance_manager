# finance_manager/db/base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .session import Base


DATABASE_URL = "sqlite:///finance.db"  # Your database URL, adjust if needed

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit from
Base = declarative_base()
