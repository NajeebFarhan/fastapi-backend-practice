from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from os import environ
from dotenv import load_dotenv

load_dotenv()

USR = environ.get("DB_USR") or ""
HOST = environ.get("HOST") or ""
PWD = environ.get("DB_PWD") or ""
PORT = environ.get("PORT") or 3306

# print(USR, HOST, PWD, PORT)

engine = create_engine(f"mysql+pymysql://{USR}:{PWD}@{HOST}:{PORT}/sakila", echo=True)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)

# used by fastapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    

        