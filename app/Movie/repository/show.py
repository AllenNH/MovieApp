from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models
from sqlalchemy.orm import Session



def create(request : schemas.show, db : Session ):
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
    return show

def update(id: int, request: schemas.movie, db: Session):
    show = db.query(models.Show).filter(models.Show.id == id)
    if not show.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Show with id {id} not found")
    
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