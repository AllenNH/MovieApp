from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database
from sqlalchemy.orm import Session
from Movie.repository import cinema_hall
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix = '/cinemaHall',
    tags = ['Cinema Hall']

)


@router.post('/add_cinemaHall')
def create(request : schemas.cinemaHall , db : Session = Depends(get_db)):
    return cinema_hall.create(request, db)


@router.get('/details',status_code=200,
            response_model=List[schemas.showCinemaHall])
def get_all_cinemahall(db : Session = Depends(get_db)):
    return cinema_hall.get_all_cinemaHall(db)

@router.get('/details/{id}', status_code=200)
def get_cinemaHall_by_id(id: int,db : Session = Depends(get_db)):
    return cinema_hall.get_cinemaHall_by_id(db,id)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.cinemaHall, db : Session = Depends(get_db)):
    return cinema_hall.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db)):
    return cinema_hall.destroy(id,db)
