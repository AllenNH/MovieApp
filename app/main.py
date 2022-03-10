from fastapi import FastAPI, Depends
from Movie import schemas, models, database
from Movie.database import  engine
from sqlalchemy.orm import Session
from Movie.routers import user, authenticate_user, cinema, movie, show, location 
from Movie.routers import booking, show_seat, cinema_hall, cinema_seat, admin, test
app = FastAPI()

models.Base.metadata.create_all(engine) 


app.include_router(authenticate_user.router)
app.include_router(user.router)
app.include_router(cinema.router)
app.include_router(movie.router)
app.include_router(show.router)
app.include_router(location.router)
app.include_router(booking.router)
app.include_router(show_seat.router)
app.include_router(cinema_hall.router)
app.include_router(cinema_seat.router)
app.include_router(admin.router)
app.include_router(test.router)