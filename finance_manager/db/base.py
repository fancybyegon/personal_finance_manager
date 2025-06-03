

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .session import Base


DATABASE_URL = "sqlite:///finance.db" 


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
