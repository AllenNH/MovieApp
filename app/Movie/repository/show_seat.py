from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from Movie import schemas, models
from datetime import datetime


def get_showSeat_by_id(db : Session, showSeat_id : int):
    return db.query(models.ShowSeat).filter(models.ShowSeat.id == showSeat_id).first()


def create(request : schemas.showSeat, db : Session ):
    new_showSeat = models.ShowSeat(status = request.status,
                                    price=request.price,
                                    cinemaSeat_id=request.cinemaSeat_id,
                                    show_id = request.show_id,
                                    booking_id=request.booking_id)                    
    db.add(new_showSeat)
    db.commit()
    db.refresh(new_showSeat)
    return new_showSeat


def get_all_showSeat(db: Session):
    
    return db.query(models.ShowSeat).all()

def update(id: int, request: schemas.showSeat, db: Session):
    showSeat = db.query(models.ShowSeat).filter(models.ShowSeat.id == id)
    if not showSeat.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id {id} not found")
    showSeat.update(request.dict())
    db.commit()
    return 'updated'

def destroy(id: int,db: Session):
    showSeat = db.query(models.ShowSeat).filter(
            models.ShowSeat.id == id)
    if not showSeat.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Show Seat with {id} is not available")
    showSeat.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'