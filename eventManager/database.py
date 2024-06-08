from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"

#Postgres connection
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:jkn;@localhost/TodoApplication"

#Db connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

#create session
sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

#declearing orm method to mapping table
Base= declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
