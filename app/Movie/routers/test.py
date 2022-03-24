
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..repository import booking
from typing import List 
from sqlalchemy.sql import func
from datetime import date, time
from typing import List, Optional

get_db = database.get_db
router = APIRouter(
    prefix = '/test',
    tags = ['Testing']

)
#testing out new query
@router.post('')
def sum_price(booking_id : int , db : Session = Depends(get_db)):
    total_amt = db.query(func.sum(models.ShowSeat.price).label('amount')).\
            filter(models.ShowSeat.booking_id == booking_id).all()
    
    print(total_amt[0].amount)

@router.post('/query', response_model=List[schemas.showCinemaMovie])
def query(title : str, location :str, Mdate : Optional[date] = None, city : Optional[str] = None, db : Session = Depends(get_db)):
    cinema  = db.query(models.Cinema).\
                join(models.CinemaHall).\
                    join(models.Show).\
                        join(models.Location).\
        filter(models.Movie.title.contains(title), models.Location.name.contains(location)).all()
    return cinema 