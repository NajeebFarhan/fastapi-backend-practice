from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from model import Account
from util.token import verify_token
from db_setup import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_account(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Account:
    payload = verify_token(token)

    username: str | None = payload.get("sub")

    user = db.query(Account).filter(Account.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
