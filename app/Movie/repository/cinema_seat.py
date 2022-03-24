from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from datetime import datetime
import re


def get_by_id(db : Session, cinemaSeat_id : int):
    return db.query(models.CinemaSeat).filter(models.CinemaSeat.id == cinemaSeat_id).first()


def create(request : schemas.cinemaSeat, db : Session, id : int, role : str):
    if role != 'admin':
        check_id = db.query(models.CinemaHall.id).\
            join(models.Cinema).\
            filter(models.Cinema.user_id == id).all()
        hall_list = [check_id[i].id for i in range(len(check_id)) ]
        if request.cinemaHall_id not in hall_list:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cinema Hall {request.cinemaHall_id } doesn't come under current user")

    seatNumRegex = re.compile(r'^[A-Z]{1,2}$')
    seat_type = ["classic","classic_plus","premium"]
    if not seatNumRegex.match(request.rowName):  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Seat Row format incorrect{request.rowName} eg: A,D,AA,GZ")
    if request.seatType not in seat_type:  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"please specify available seat type (classic/classic_plus/premium)")

    seat_ids = []
    seats_present = db.query(models.CinemaSeat.seatNo).filter(models.CinemaSeat.cinemaHall_id == id).all()
    seat_list = [seats_present[i].seatNo for i in range(len(seats_present)) ]
    for seatNum in range(1,request.noOfSeats+1):
        
        seatNo = request.rowName + "-" + str(seatNum)     
        if seatNo not in seat_list:   
            new_cinemaSeat = models.CinemaSeat(seatNo=seatNo, 
                                                seatType=request.seatType,
                                                flag=1,
                                                cinemaHall_id=request.cinemaHall_id)                    
            db.add(new_cinemaSeat)
            db.commit()
            db.refresh(new_cinemaSeat)
            seat_ids.append(new_cinemaSeat.id)
    return f"seats added with ids{seat_ids}"

def get_all(db: Session):    
    return db.query(models.CinemaSeat).all()

def get_user_cinemaSeat(cinemaHall_id: int, db: Session, id : int, role : str):
    if role != 'admin':
        check_id = db.query(models.CinemaHall.id).\
            join(models.Cinema).\
            filter(models.Cinema.user_id == id).all()
        hall_list = [check_id[i].id for i in range(len(check_id)) ]
        if cinemaHall_id not in hall_list:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cinema Hall {cinemaHall_id } doesn't come under current user")
        
        
    return db.query(models.CinemaSeat).\
        filter(models.CinemaSeat.cinemaHall_id == cinemaHall_id).all()



def update(cinemaSeat_id: int, request : schemas.cinemaSeat, db: Session, id : int, role : str):
    if role != 'admin':
        check_id = db.query(models.CinemaSeat.id).\
            join(models.CinemaHall).\
            join(models.Cinema).\
            filter(models.Cinema.user_id == id).all()
        seat_list = [check_id[i].id for i in range(len(check_id)) ]
        print(seat_list)
        if cinemaSeat_id not in seat_list:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cinema Hall {cinemaSeat_id } doesn't come under current user")

        
        
        seatNumRegex = re.compile(r'^[A-Z]{1,2}-[0-9]{1,2}$')
        seat_type = ["classic","classic_plus","premium"]
        if not seatNumRegex.match(request.seatNo):  
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Seat number format incorrect{request.seatNo} eg: A-1,D-22,AA-1,GZ-99")
        if request.seatType not in seat_type:  
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"please specify available seat type (classic/classic_plus/premium)")

    cinemaSeat = db.query(models.CinemaSeat).filter(models.CinemaSeat.id == cinemaSeat_id)
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