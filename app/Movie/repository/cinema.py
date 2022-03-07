from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models
from sqlalchemy.orm import Session


def get_cinema_by_id(db: Session, cinema_id: int):
    return db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()

def get_cinema_by_name(db: Session, name: str):
    return db.query(models.Cinema).filter(models.Cinema.name == name).first()


def create(request : schemas.cinema, db : Session ):
    new_cinema = models.Cinema(name=request.name,
                noOfScreens=request.noOfScreens,
            user_id = 0,location_id = 0)
    db.add(new_cinema)
    db.commit()
    db.refresh(new_cinema)
    return new_cinema


def show(id: int, db : Session):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == id).first()
    if not cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return cinema 


def update(id: int, request: schemas.cinema, db : Session):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == id).first()
    if not cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")
    cinema.update(request.dict())
    db.commit()
    return cinema