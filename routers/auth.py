from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db_setup import get_db
from util.password_auth import hash_password, verify_password