from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql://root:Hammad1999@localhost/card_game"
engine = create_engine(DATABASE_URL, pool_size=100, max_overflow=100, pool_timeout=60)

# Create a session class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def connect():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()