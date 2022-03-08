from turtle import circle
from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from Movie.repository import location
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix='/location',
    tags=["Location"]
)



@router.post('/add_location')
def create(request : schemas.location , db : Session = Depends(get_db)):
    db_location = location.get_location_by_name(db, request.name)
    if db_location:
        raise HTTPException(status_code=400, 
                detail=f"Movie with name{request.title} already exists")
    return location.create(request, db)


@router.get('/location_details',status_code=200,
            response_model=List[schemas.showLocation])
def get_all_location(db : Session = Depends(get_db)):
    return location.get_all_location(db)

@router.get('/location_details/{name}', status_code=200)
def get_location_by_name(name: str, 
                db : Session = Depends(get_db)):
    return location.get_location_by_name(db,name)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.location, db : Session = Depends(get_db)):
    return location.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db)):
    return location.destroy(id,db)

