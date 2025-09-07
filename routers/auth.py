from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import Annotated

from db_setup import get_db
from util.password_auth import hash_password, verify_password
from util.token import create_token
from model import Account


router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(first_name: Annotated[str, Form()], last_name: Annotated[str, Form()], username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):

    if db.query(Account).filter(Account.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    account = Account(first_name=first_name, last_name=last_name, username=username, hashed_password=hash_password(password))
    db.add(account)
    db.commit()
    db.refresh(account)
    return {"msg": "Account created"}


@router.post("/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):

    account = db.query(Account).filter(Account.username == username).first()

    if not account or not verify_password(password, account.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(account.username)
    
    return {"access_token": token, "token_type": "bearer"}