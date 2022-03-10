from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import user
from typing import List

get_db = database.get_db
router = APIRouter(
    prefix='/user',
    tags=["Users"]
)


@router.post('/sign_up',
        response_model=schemas.showUser, status_code=status.HTTP_201_CREATED)
def create(request : schemas.user, db : Session = Depends(get_db)):
    db_user = user.get_user_by_phone_no(db, phone=request.phone)
    if db_user:
        raise HTTPException(status_code=400, 
                detail=f"Account with {request.phone} already exists")
    return user.create(request, db)


@router.get('/user_details', status_code=200)
def get_user_details(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
    return user.get_user_by_id(db, current_user.id)



@router.put('/update_user_details', status_code=202)
def update(request : schemas.user, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
        pass

@router.get('/user_details/{id}', status_code=200)
def get_user_details(id: int,db : Session = Depends(get_db)):
    #only for admin
    return user.get_user_by_id(db, id)


@router.delete('/delete_user/{id}', status_code=204)
def destroy(id, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
        #only for admin
    pass

@router.get('/user_details_all', status_code=200,
                response_model=List[schemas.showUser])
def get_user_details(db : Session = Depends(get_db)):
    return user.get_all(db)