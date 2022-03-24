
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from datetime import datetime


def get_movie_by_name(db : Session, movie_name : str):
    return db.query(models.Movie).\
        filter(models.Movie.title.contains(movie_name)).first()


def get_movie_by_id(db : Session, movie_id : int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def create(request : schemas.movie, db : Session, id: int ):
    new_movie = models.Movie(title=request.title,
                description=request.description,
                duration=request.duration,
                language=request.language,
                genre=request.genre,
                user_id = id,
                status = request.status,
                timestamp = datetime.utcnow())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


def get_all_movie(db: Session):
    movie = db.query(models.Movie).all()
    return movie

def update(title : str, request: schemas.movie, db: Session, id : int):
    movie = db.query(models.Movie).filter(models.Movie.title == title)
    if not movie.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Movie with title {title} not found")
    movie_exist = db.query(models.Movie).filter(models.Movie.title == request.title).first()
    if  movie_exist and movie_exist.title != request.title:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Movie with title {title} already present")
    movie.update(request.dict())
    movie.user_id = id
    db.commit()
    return 'updated'

def destroy(title: str,db: Session):
    movie = db.query(models.Movie).filter(
            models.Movie.title == title)
    if not movie.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Movie with name {title} is not available")
    movie.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

def get_all_current_movie(db: Session):
    movie = db.query(models.Movie).filter(models.Movie.status == True).all()
    return movie


def get_all_current_movie_by_location(db: Session, location :str):
    movie = db.query(models.Movie).\
        join(models.Show).\
            join(models.CinemaHall).\
                join(models.Cinema).\
                    join(models.Location).\
        filter(models.Movie.status == True, models.Location.name.contains(location)).all()
    
    return movie

def change_status(id :int, status : bool, db: Session):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Movie with the id {id} is not found")
    
    movie.status = status

    db.commit()

    return {"msg":"status updated"}