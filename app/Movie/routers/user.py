from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import user
from typing import List
import re

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
    phoneNumRegex = re.compile(r'^(\+[0-9]{2}[- ]?)?[0-9]{10}$')
    if not phoneNumRegex.match(str(request.phone)):
        raise HTTPException(status_code=400, 
                detail=f"Phone number invalid {request.phone} ")
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
def get_user_details(id: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    #only for admin
    return user.get_user_by_id(db, id)


@router.delete('/delete_user/{id}', status_code=200)
def destroy(id, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
        
        if id == str(current_user.id):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Can't delete own account")
        return user.destroy(db, id)
 

@router.get('/user_details_all', status_code=200,
                response_model=List[schemas.showUser])
def get_user_details(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return user.get_all(db)