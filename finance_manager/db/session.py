from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# Define the SQLite database URL (relative path)
DATABASE_URL = "sqlite:///finance.db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite and threaded apps
)

# Create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Create a Base class for models to inherit from
Base = declarative_base()

# Dependency function for getting DB session (if needed later in APIs)
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables if not exist (optional: only if you want to create tables without migrations)
def init_db():
    import finance_manager.db.models  # Ensure models are imported before metadata create
    Base.metadata.create_all(bind=engine)
    from .session import Base

