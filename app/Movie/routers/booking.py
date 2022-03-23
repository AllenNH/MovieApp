from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database, oauth2
from sqlalchemy.orm import Session
from Movie.repository import booking
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix = '/booking',
    tags = ['Booking']

)


@router.post('/add_booking',response_model = schemas.showPayment)
def create(request : schemas.booking , db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
    if request.noOfseats != len(request.seat_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Number of seats and seat ids must match")
    return booking.create(request, db, current_user.id)


@router.get('/booking_details',status_code=200,
            response_model=List[schemas.showPayment])
def get_user_booking(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
    return booking.get_user_booking(db, current_user.id)

@router.get('/booking_details/{id}', status_code=200)
def get_booking_by_id(id: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return booking.get_booking_by_id(db,id)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.booking, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return booking.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return booking.destroy(id,db)






