
from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database, models
from sqlalchemy.orm import Session
from Movie.repository import booking
from typing import List 
from sqlalchemy.sql import func
from datetime import date, time

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
def query(movie_name : str,Mdate : date, city : 
            str, db : Session = Depends(get_db)):
    shows = db.query(models.Cinema.name).join(models.CinemaHall).\
                join(models.Show).join(models.Movie).\
                    filter(models.Movie.title.contains(movie_name)).\
                        order_by(models.Movie.timestamp)
    
    print(shows.all())
