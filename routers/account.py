from sqlalchemy import text
from sqlalchemy.orm import Session, load_only
from fastapi import APIRouter, HTTPException, Depends, Form
from typing import Annotated

from schema import AccountSchema, CurrentAccountSchema
from model import Account
from db_setup import get_db
from util.password_auth import verify_password, hash_password
from util.current_account import get_current_account

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountSchema])
async def get_accounts(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):

    accounts = (
        db.query(Account)
        .options(
            load_only(
                Account.actor_id,
                Account.first_name,
                Account.last_name,
                Account.username,
            )
        )
        .limit(limit)
        .offset(offset)
        .all()
    )

    return accounts


@router.get("/me", response_model=CurrentAccountSchema)
async def get_my_account(current_account: Account = Depends(get_current_account)):
    return current_account


@router.put("/changepassword", response_model=CurrentAccountSchema)
async def change_password(password: Annotated[str, Form()], new_password: Annotated[str, Form()], db: Session = Depends(get_db), current_account: Account = Depends(get_current_account)):
    
    if not verify_password(password, current_account.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    current_account.hashed_password = hash_password(new_password)
    
    db.commit()
    
    return current_account
    

@router.get("/count")
async def get_count(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT COUNT(*) FROM actor")).scalar()

    return {"count": result}


@router.get("/{account_id}", response_model=AccountSchema)
async def get_actor(
    account_id: int,
    db: Session = Depends(get_db),
):

    account = (
        db.query(Account)
        .options(
            load_only(
                Account.actor_id,
                Account.first_name,
                Account.last_name,
                Account.username,
            )
        )
        .filter(Account.actor_id == account_id)
        .first()
    )

    if account:
        return account

    else:
        raise HTTPException(status_code=404, detail="Account not found")


@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):

    if not current_account.is_admin:
        raise HTTPException(status_code=401, detail="Unathorized action")

    account = db.query(Account).filter(Account.actor_id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    else:
        db.delete(account)
        db.commit()

        return {"message": f"Account {account_id} successfully deleted"}
