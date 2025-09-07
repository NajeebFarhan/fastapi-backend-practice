from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import Annotated

from db_setup import get_db
from util.password_auth import hash_password, verify_password
from util.token import create_token
from model import User


router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User created"}


@router.post("/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.username)
    
    return {"access_token": token, "token_type": "bearer"}