from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///finance.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()



def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import finance_manager.db.models  
    Base.metadata.create_all(bind=engine)
    from .session import Base

