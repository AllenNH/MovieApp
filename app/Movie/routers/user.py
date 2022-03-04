from fastapi import APIRouter, Depends, status, HTTPException, Response
from Movie import schemas, models, database, oauth2
from Movie.hashing import Hash 
from sqlalchemy.orm import Session
from Movie.repository import user

get_db = database.get_db
router = APIRouter(
    prefix='/user',
    tags=["Users"]
)


@router.post('/sign_up',response_model=schemas.ShowUser)
def create(request : schemas.user, db : Session = Depends(get_db)):
    db_user = user.get_user_by_phone_no(db, phone=request.phone)
    if db_user:
        raise HTTPException(status_code=400, 
                detail=f"Account with {request.phone} already exists")
    return user.create(request, db)


@router.get('/user_details')
def get_useer_details(db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.get_current_user)):
    return user.get_user_by_id(db, current_user.id)
