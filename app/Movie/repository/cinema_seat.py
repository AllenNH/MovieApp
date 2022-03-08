from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from Movie import schemas, models
from datetime import datetime


def get_by_id(db : Session, cinemaSeat_id : int):
    return db.query(models.CinemaSeat).filter(models.CinemaSeat.id == cinemaSeat_id).first()


def create(request : schemas.cinemaSeat, db : Session ):
    new_cinemaSeat = models.CinemaSeat(seatNo=request.seatNo, 
                                        seatType=request.seatType,
                                        flag=request.flag,
                                        cinemaHall_id=request.cinemaHall_id)                    
    db.add(new_cinemaSeat)
    db.commit()
    db.refresh(new_cinemaSeat)
    return new_cinemaSeat

def get_all(db: Session):    
    return db.query(models.CinemaSeat).all()

def update(id: int, request: schemas.cinemaSeat, db: Session):
    cinemaSeat = db.query(models.CinemaSeat).filter(models.CinemaSeat.id == id)
    if not cinemaSeat.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seat with id {id} not found")
    cinemaSeat.update(request.dict())
    db.commit()
    return 'updated'

def destroy(id: int,db: Session):
    cinemaSeat = db.query(models.CinemaSeat).filter(
            models.CinemaSeat.id == id)
    if not cinemaSeat.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Seat with {id} is not available")
    cinemaSeat.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'