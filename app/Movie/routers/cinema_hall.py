from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database, oauth2
from sqlalchemy.orm import Session
from Movie.repository import cinema_hall
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix = '/cinemaHall',
    tags = ['Cinema Hall']

)


@router.post('/add_cinemaHall')
def create(request : schemas.cinemaHall , db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema_hall.create(request, db, current_user.id, current_user.role)

@router.get('/details', status_code=200, response_model = List[schemas.showCinemaHall])
def get_cinema_hall_details(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema_hall.get_cinemaHall_by_id(db,current_user.id)

'''
@router.get('/details',status_code=200,response_model=List[schemas.showCinemaHall])
def get_all_cinemahall(db : Session = Depends(get_db)):
    return cinema_hall.get_all_cinemaHall(db)
'''
@router.get('/details/{id}', status_code=200)
def get_cinemaHall_by_id(id: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_hall.get_cinemaHall_by_id(db,id)

@router.put('/edit', status_code=202)
def update(request : schemas.cinemaHall, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema_hall.update(current_user.id,request,db)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.cinemaHall, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_hall.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema_hall.destroy(id,db)
