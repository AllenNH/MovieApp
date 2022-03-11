from tkinter import N
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

def setup_seat(classic, classic_plus, premium,
                                    show_id, cinemaHall_id, db, id: int, role: str):
    if role != 'admin':
        check_user = db.query(models.Cinema.user_id).\
            join(models.CinemaHall).\
            join(models.Show).\
            filter(models.Show.id ==  show_id).first()
        try:
            if id != check_user[0]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Show with id {show_id} doesn't belong to current user")
            check_user = db.query(models.Cinema.user_id).\
                join(models.CinemaHall).\
                filter(models.CinemaHall.id ==cinemaHall_id).first()
            
            if id != check_user[0]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Cinema Hall id: {cinemaHall_id } doesn't belong to current user")
        except: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"cinemaHall id or show id is not present")

        
        
    cinema_seats= db.query(models.CinemaSeat
                ).filter(models.CinemaSeat.cinemaHall_id == cinemaHall_id).all()  
    price = {"classic": classic,
            "classic_plus": classic_plus,"premium": premium}
    print(price)
    
    for seat in cinema_seats:
        request = schemas.showSeat(status=0,price=price.get(seat.seatType,0),
                                    cinemaSeat_id=seat.id,
                                    show_id=show_id,booking_id=0)
        print(create(request, db))