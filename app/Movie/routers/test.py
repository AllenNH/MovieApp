
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