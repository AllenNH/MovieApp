from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models
from sqlalchemy.orm import Session
from Movie.repository import movie
from datetime import datetime, time
from sqlalchemy import or_, and_


def create(request : schemas.show, db : Session, id : int, role : str):
    if role != 'admin':
        check_user = db.query(models.Cinema.user_id).\
            join(models.CinemaHall).\
            filter(models.CinemaHall.id ==request.cinemaHall_id).first()
        if id != check_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cinema Hall id {request.cinemaHall_id } doesn't belong to current user")
        check_movie = movie.get_movie_by_id(db, request.movie_id)
        if check_movie is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Movie with id {request.movie_id} is not present")

        check_hall = db.query(models.CinemaHall).\
                            join(models.Show).\
            filter(models.Show.showDate
                         == datetime.fromisoformat(str(request.showDate)),
                         models.Show.cinemaHall_id == request.cinemaHall_id,
                or_(and_(models.Show.startTime <= time.fromisoformat(str(request.startTime)),
                models.Show.endTime >= time.fromisoformat(str(request.startTime))),
                and_(models.Show.startTime <= time.fromisoformat(str(request.endTime)),
                models.Show.endTime >= time.fromisoformat(str(request.endTime)))))
        print(check_hall)
        print(check_hall.first())
        if check_hall.first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Movie hall is booked for the specified time")


    
    new_show = models.Show(showDate=request.showDate,
                startTime=request.startTime,
                endTime=request.endTime,
                cinemaHall_id=request.cinemaHall_id,
                movie_id=request.movie_id)
    db.add(new_show)
    db.commit()
    db.refresh(new_show)
    return new_show


def get_all_show(db: Session):
    show = db.query(models.Show).all()
    return show

def get_show_by_id(id: int,db: Session):
    show = db.query(models.Show).filter(models.Show.id == id)
    if not show.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Show with id {id} not found")
    return show.first()

def update(id: int, request: schemas.movie, db: Session, user_id: int, role : str):
    show = db.query(models.Show).filter(models.Show.id == id)
    if not show.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Show with id {id} not found")
    if role != 'admin':
        check_user = db.query(models.Cinema.user_id).\
            join(models.CinemaHall).\
            filter(models.CinemaHall.id ==request.cinemaHall_id).first()
        if  user_id != check_user[0]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cinema Hall id {request.cinemaHall_id } doesn't belong to current user")
        check_movie = movie.get_movie_by_id(db, request.movie_id)
        if check_movie is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Movie with id {request.movie_id} is not present")
    
    
    show.update(request.dict())
    db.commit()
    return 'updated'

def delete(id: int,db: Session):
    show = db.query(models.Show).filter(
            models.Show.id == id)
    if not show.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"show with id {id} is not available")
    show.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

def get_by_name(name,db: Session):
    show = db.query(models.Show).join(models.Movie).filter(models.Movie.title == name).all()
    return show