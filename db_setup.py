from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:261111@localhost:3306/sakila", echo=True)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)

# used by fastapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# this is for some manual db changing
if __name__ == "__main__":
    pass