from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import cinema_seat
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix = '/cinemaSeat',
    tags = ['Cinema Seat']

)


@router.post('/add_cinemaSeat')
def create(request : schemas.cinemaSeatAddRow , db : Session = Depends(get_db),
       current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema_seat.create(request, db, current_user.id, current_user.role)


@router.get('/details',status_code=200)
def get_all_cinema_seats(cinemaHall_id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema_seat.get_user_cinemaSeat(cinemaHall_id, 
                        db, current_user.id, current_user.role)



@router.get('/details/all',status_code=200,
            response_model=List[schemas.showCinemaSeat])
def get_all_cinema_seats(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_seat.get_all(db)

@router.get('/details/{id}', status_code=200)
def get_cinemaSeat_by_id(id: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_seat.get_by_id(db,id)

@router.put('/edit', status_code=202)
def update(cinemaSeat_id: int,request : schemas.cinemaSeat, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema_seat.update(cinemaSeat_id, request, 
                        db, current_user.id, current_user.role)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.cinemaSeat, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_seat.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_seat.destroy(id,db)
