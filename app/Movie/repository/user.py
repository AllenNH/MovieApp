from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models
from ..hashing import Hash 
from sqlalchemy.orm import Session
from datetime import datetime


def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                    detail = f"User with id {user_id} is not available")
    return user

def get_user_by_phone_no(db: Session, phone: int):
    return db.query(models.User).filter(models.User.phone == phone).first()


def create(request : schemas.user, db : Session ):
    new_user = models.User(name=request.name,phone=request.phone,
                        hashed_password=Hash.bcrypt(request.password),
                        timestamp = datetime.utcnow()) 
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


def update(id: int, request: schemas.user, db : Session):
    print("Hello")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")
    
    user.update(request.dict())
    db.commit()
    return user

def destroy(db: Session, id : int):
    movie = db.query(models.User).filter(
            models.User.id == id)
    if not movie.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} is not available")
    movie.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

def get_all(db):
    return db.query(models.User).all()