from fastapi import FastAPI, Depends

from .Movie import schemas, models, database, run_scheduled_task
from .Movie.database import  engine
from sqlalchemy.orm import Session
from .Movie.routers import user, authenticate_user, cinema, movie, show, location 
from .Movie.routers import booking, show_seat, cinema_hall, cinema_seat, admin, test
from fastapi_utils.tasks import repeat_every


app = FastAPI()

#models.Base.metadata.create_all(engine) 

@app.on_event("startup")
@repeat_every(seconds=60*60*24 )  # 24 hour
def scheduled_task():
    print("he")
    run_scheduled_task.clear_old_movie()
    pass


app.include_router(authenticate_user.router)
app.include_router(user.router)
app.include_router(admin.router)

app.include_router(movie.router)


app.include_router(location.router)
app.include_router(cinema.router)
app.include_router(cinema_hall.router)
app.include_router(cinema_seat.router)



app.include_router(show.router)
app.include_router(show_seat.router)


app.include_router(booking.router)

app.include_router(test.router)