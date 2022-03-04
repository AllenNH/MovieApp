from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_phone_no(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def create(request : schemas.user, db : Session ):
    new_user = models.User(name=request.name,phone=request.phone,
                        hashed_password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db : Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user