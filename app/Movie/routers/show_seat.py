from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database, oauth2
from sqlalchemy.orm import Session
from Movie.repository import show_seat
from typing import List 

get_db = database.get_db
router = APIRouter(
    prefix = '/showSeat',
    tags = ['Show Seat']

)


@router.post('/add_showSeat')
def create(request : schemas.showSeat , db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return show_seat.create(request, db)


@router.get('/details',status_code=200,
            response_model=List[schemas.showShowSeat])
def get_all_showSeat(db : Session = Depends(get_db)):
    print("a")
    return show_seat.get_all_showSeat(db)

@router.get('/details/{id}', status_code=200)
def get_showSeat_by_id(id: int,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return show_seat.get_showSeat_by_id(db,id)

@router.put('/edit/{id}', status_code=202)
def update(id: int,request : schemas.showSeat, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return show_seat.update(id,request,db)


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return show_seat.destroy(id,db)

@router.post('/setup_seat')
def setup_seat(classic: float,classic_plus: float,premium: float,
                show_id: int,
                db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_merchant)):
    
    return show_seat.setup_seat(classic, classic_plus, premium,
                                    show_id, db, 
                                        current_user.id, current_user.role)

