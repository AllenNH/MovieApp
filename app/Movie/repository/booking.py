from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from Movie import schemas, models
from datetime import datetime


def get_booking_by_id(db : Session, Booking_id : int):
    return db.query(models.Booking).filter(models.Booking.id == Booking_id).first()


def create(request : schemas.booking, db : Session ):
    new_booking = models.Booking(noOfseats=request.noOfseats,
                    timestamp = datetime.utcnow(),
                    status = request.status,
                    user_id = request.user_id,
                    show_id = request.show_id)                    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def get_all_booking(db: Session):
    location = db.query(models.Booking).all()
    return location

def update(id: int, request: schemas.booking, db: Session):
    booking = db.query(models.Booking).filter(models.Booking.id == id)
    if not booking.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id {id} not found")
    booking.update(request.dict())
    db.commit()
    return 'updated'

def destroy(id: int,db: Session):
    booking = db.query(models.Booking).filter(
            models.Booking.id == id)
    if not booking.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Booking with {id} is not available")
    booking.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'