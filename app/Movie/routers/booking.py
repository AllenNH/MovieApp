from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database
from sqlalchemy.orm import Session
from Movie.repository import booking
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix = '/booking',
    tags = ['Booking']

)


@router.post('/add_booking')
def create(request : schemas.booking , db : Session = Depends(get_db)):
    return booking.create(request, db)


@router.get('/booking_details',status_code=200,
            response_model=List[schemas.showBooking])
def get_all_booking(db : Session = Depends(get_db)):
    return booking.get_all_booking(db)

@router.get('/details_details/{id}', status_code=200)
def get_booking_by_id(id: int,db : Session = Depends(get_db)):
    return booking.get_booking_by_id(db,id)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.booking, db : Session = Depends(get_db)):
    return booking.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db)):
    return booking.destroy(id,db)