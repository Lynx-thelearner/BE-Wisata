from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_TRANSACTION = os.getenv("DATABASE_TRANSACTION")
DATABASE_SESSION = os.getenv("DATABASE_SESSION")

try:
    #buat coba ke Transaction pooler
    engine = create_engine(DATABASE_TRANSACTION, pool_pre_ping=True)
    with engine.connect() as conn:
        print("Connected via Transaction pooler")
except Exception as e:
    print(f"gagal konek via Trasaction pooler, mencoba Session pooler...")
    try:
        #buat coba session pooler
        engine = create_engine(DATABASE_SESSION, pool_pre_ping=True)
        with engine.connect() as conn:
            print("Connected via pooler")
    except Exception as e1:
        print("Both connections failed.")
        print(f"Transaction error: {e}")
        print(f"Session error: {e1}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()