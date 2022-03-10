from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import admin
from typing import List

get_db = database.get_db
router = APIRouter(
    prefix='/admin',
    tags=["Admin"]
)




@router.put('/change_privilege/{id}', status_code=202)
def get_user_details(id: int,role: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    if current_user.id == id:
        raise  HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"user cant change his own privilege")
    return admin.update(id,role,db)

'''
@router.put('/update_user_details', status_code=202)
def update(request : schemas.user, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
        pass

@router.get('/user_details/{id}', status_code=200)
def get_user_details(id: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    #only for admin
    return user.get_user_by_id(db, id)


@router.delete('/delete_user/{id}', status_code=204)
def destroy(id, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
        #only for admin
    pass

@router.get('/user_details_all', status_code=200,
                response_model=List[schemas.showUser])
def get_user_details(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return user.get_all(db)
'''