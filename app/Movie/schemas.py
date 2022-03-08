from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

from Movie.models import CinemaSeat

class user(BaseModel):
    
    name : str
    phone : int 
    password : str



    

class TokenData(BaseModel):
    id : Optional[int] = None
    role : Optional[str] = None
    name: Optional[str] = None


class cinema(BaseModel):

    name : str 
    noOfScreens : int

class showCinema(BaseModel):
    id: int
    name : str 
    noOfScreens : int
    class Config():
        orm_mode = True


class movie(BaseModel):
    title : str
    description : str
    duration : int
    language : str
    genre : str
    
    

class showMovie(BaseModel):
    title : str
    description : str
    duration : int
    language : str
    genre : str
    
    class Config():
        orm_mode = True

class show(BaseModel):
    showDate : date
    startTime :  time
    endTime : time
    cinemaHall_id : int
    movie_id : int

class showShow(BaseModel):

    id : int
    showDate : date
    startTime :  time
    endTime : time
    cinemaHall_id : int
    movie_id : int
    
    class Config():
        orm_mode = True

class location(BaseModel):

    name : str
    state : str
    pincode : int

class showLocation(BaseModel):

    id : int
    name : str
    state : str
    pincode : int

    class Config():
        orm_mode = True

class booking(BaseModel):
    noOfseats : int
    status : int
    user_id : int
    show_id : int 


class showBooking(BaseModel):
    id: int
    noOfseats : int
    status : bool
    user_id : int
    show_id : int 

    class Config():
        orm_mode = True
 
class showSeat(BaseModel):
    status: bool
    price : float
    cinemaSeat_id : int
    show_id : int
    booking_id : int 

class showShowSeat(BaseModel):
    status: bool
    price : float
    cinemaSeat_id : int
    show_id : int
    booking_id : int 

    class Config():
        orm_mode = True
 
class cinemaHall(BaseModel):
     name : str
     totalSeats : int 
     cinema_id : int 

class showCinemaHall(BaseModel):
    id: int
    name : str
    totalSeats : int
    cinema_id : int 

    class Config():
        orm_mode = True
     
class cinemaSeat(BaseModel):
    seatNo : str 
    seatType : int
    flag : int 
    cinemaHall_id :int 

class showCinemaSeat(BaseModel):
    seatNo : str 
    seatType : int
    flag : int 
    cinemaHall_id :int  

    class Config():
        orm_mode = True

class showUser(BaseModel):
    id : int
    phone : int
    name : str
    bookings : List[showBooking] = []
    
    class Config():
        orm_mode = True