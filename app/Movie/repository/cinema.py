from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from datetime import datetime
from sqlalchemy import func


def get_cinema_by_id(db: Session, cinema_id: int):
    return db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()

def get_cinema_by_name(db: Session, name: str):
    return db.query(models.Cinema).filter(models.Cinema.name == name).first()


def create(request : schemas.cinema, db : Session, id: int ):
    
    new_cinema = models.Cinema(name=request.name,
                noOfScreens=request.noOfScreens,
            user_id = id,
            location_id = request.location_id)
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


def update(cid: int, request: schemas.cinema, db : Session, user_id :int, role: str):
    new_cinema = db.query(models.Cinema).filter(models.Cinema.id == cid)
    if role != "admin":
        if new_cinema[0].user_id != user_id: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Cinema with id {cid} is not owned by user")
    if not new_cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")    
    new_cinema.update(request.dict())
    db.commit()
    return "updated"

def get_all(db: Session):    
    return db.query(models.Cinema).all()


def destroy(id: int,db: Session):
    cinema = db.query(models.Cinema).filter(
            models.Cinema.id == id)
    if not cinema.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Cinema with {id} is not available")
    cinema.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

def get_cinema_details_by_movie(db : Session, id, location , showDate):
    cinema  = db.query(models.Show).\
                join(models.CinemaHall).\
                    join(models.Cinema).\
                        join(models.Movie).\
                        join(models.Location).\
        filter(models.Movie.id == id, 
                    models.Location.name.contains(location), 
                    models.Movie.status == 1,
                    func.date(models.Show.showDate) == showDate,
                    models.Show.status == True).all()
    return cinema 