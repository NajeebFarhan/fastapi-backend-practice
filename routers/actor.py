from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends

from schema import ActorSchema, ActorCreate
from model import Actor, User
from db_setup import get_db
from datetime import datetime, timezone
from util.get_current_user import get_current_user

router = APIRouter(
    prefix="/actors",
    tags=["actors"]
)

@router.get("/", response_model=list[ActorSchema])
async def get_actors(limit: int = 10, offset: int = 0, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    actors = db.query(Actor).limit(limit).offset(offset).all()

    return actors


@router.post("/", response_model=ActorSchema)
async def post_actor(actor: ActorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Unathorized action")

    new_actor = Actor(
        first_name = actor.first_name,
        last_name = actor.last_name,
        last_update = datetime.now(timezone.utc)
    )

    db.add(new_actor)
    db.commit()
    db.refresh(new_actor)

    return new_actor


@router.get("/count")
async def get_count(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.execute(text("SELECT COUNT(*) FROM actor")).scalar()

    return { "count": result }


@router.get("/{actor_id}", response_model=ActorSchema)
async def get_actor(actor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()
    
    if actor:
        return actor
    
    else:
        raise HTTPException(status_code=404, detail="Actor not found")


@router.delete("/{actor_id}")
async def delete_actor(actor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Unathorized action")

    actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    else:
        db.delete(actor)
        db.commit()

        return { "message": f"Actor {actor_id} successfully deleted" }
