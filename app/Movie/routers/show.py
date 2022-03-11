from turtle import circle
from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from Movie.repository import show
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix='/show',
    tags=["Show"]
)



@router.post('/add_show')
def create(request : schemas.show, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return show.create(request, db, current_user.id, current_user.role)

@router.get('/show_details',status_code=200,
            response_model=List[schemas.showShow])
def get_all_show(db : Session = Depends(get_db)):
    return show.get_all_show(db)

@router.put('/edit')
def update(id: int,request : schemas.show, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    return show.update(current_user.id,request,db)

@router.put('/edit/{id}')
def update(id: int,request : schemas.show, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return show.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return show.delete(id,db)


@router.get('/search_Movie',status_code=200,
            response_model=List[schemas.showShow])
def get_show_by_movie_name(name: str,db : Session = Depends(get_db)):
    return show.get_by_name(name, db)