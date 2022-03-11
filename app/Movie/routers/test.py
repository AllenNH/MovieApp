
from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database, models
from sqlalchemy.orm import Session
from Movie.repository import booking
from typing import List 
from sqlalchemy.sql import func

get_db = database.get_db
router = APIRouter(
    prefix = '/test',
    tags = ['Testing']

)

@router.post('')
def sum_price(booking_id : int , db : Session = Depends(get_db)):
    total_amt = db.query(func.sum(models.ShowSeat.price).label('amount')).\
            filter(models.ShowSeat.booking_id == booking_id).all()
    
    print(total_amt[0].amount)

@router.post('/query')
def query(id : int , db : Session = Depends(get_db)):
    check_user = db.query(models.Cinema.user_id).\
            join(models.CinemaHall).\
            join(models.Show).\
            filter(models.Show.id ==id).first()
    #cinema_list = [check_id[i].user_id for i in range(len(check_id)) ]
    print(check_user[0])
