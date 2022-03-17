from turtle import circle
from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import cinema
from typing import List

get_db = database.get_db
router = APIRouter(
    prefix='/cinema',
    tags=["Cinema"]
)


@router.post('/add_cinema')
def create(request : schemas.cinema, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    db_user = cinema.get_cinema_by_name(db, name=request.name)
    if db_user:
        raise HTTPException(status_code=400, 
                detail=f"Cinema with name{request.name} already exists")
    return cinema.create(request, db, current_user.id)


@router.get('/cinema_details',
                    response_model=List[schemas.showCinema])
def get_cinema_details(db : Session = Depends(get_db)):
    return cinema.get_all(db)


@router.put('/update_details', status_code=202)
def update(id: int,request : schemas.cinema, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return cinema.update(id,request,db, current_user.id, current_user.role)

@router.put('/update_details/{id}', status_code=202)
def update(id: int,request : schemas.cinema, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema.update(id,request,db, current_user.id, current_user.role)

@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return cinema.destroy(id,db)




@router.post('/cinema_details_s', response_model=List[schemas.showCinemaMovie])
def get_cinema_details_by_movie(id : int, location: str, db : Session = Depends(get_db)):
    print("form cinemaMovies")
    return cinema.get_cinema_details_by_movie(db, id, location)

