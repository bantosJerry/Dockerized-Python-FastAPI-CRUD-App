from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import User, Base

# Load environment variables
load_dotenv()

# Read PostgreSQL credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "db") 
DB_USER = os.getenv("DB_USER", "user") 
DB_PASSWORD = os.getenv("DB_PASSWORD", "password") 
DB_NAME = os.getenv("DB_NAME", "python_fastapi_crud_db") 
DB_PORT = os.getenv("DB_PORT", "5432") 

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize database connection
engine = create_engine(DATABASE_URL)

# Set up the sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Drop the table if needed (be cautious)
# To drop the "users" table, uncomment the following line
# def drop_table():
#     User.__table__.drop(engine)

# drop_table()

def check_and_create_table():
    # Reflect the existing tables in the database
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names(): 
        print("Table doesn't exist, creating it...")
        print(Base.metadata.tables)
        Base.metadata.create_all(engine) 
    else:
        print("Table already exists.")

check_and_create_table()
