from turtle import circle
from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import cinema

get_db = database.get_db
router = APIRouter(
    prefix='/cinema',
    tags=["Cinema"]
)


@router.post('/sign_up')
def create(request : schemas.cinema, db : Session = Depends(get_db)):
    db_user = cinema.get_cinema_by_name(db, name=request.name)
    if db_user:
        raise HTTPException(status_code=400, 
                detail=f"Account with {request.name} already exists")
    return cinema.create(request, db)



@router.get('/cinema_details')
def get_user_details(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
    pass



@router.put('/update_cinema_details', status_code=202)
def update(request : schemas.user, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
    pass


@router.delete('/delete_cinema/{id}', status_code=204)
def destroy(id, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
        #only for admin
    pass

@router.get('/cinema_details/{id}', status_code=200)
def get_useer_details(id: int,db : Session = Depends(get_db)):
    #only for admin
    return cinema.get_user_by_id(db, id)
