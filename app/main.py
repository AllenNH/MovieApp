from fastapi import FastAPI, Depends
from Movie import schemas, models, database
from Movie.database import  engine
from sqlalchemy.orm import Session
from Movie.routers import user, authenticate_user, cinema, movie, show, location 
from Movie.routers import booking, show_seat, cinema_hall, cinema_seat, admin, test
from fastapi_utils.tasks import repeat_every

from example_scheduler import arq_worker

app = FastAPI()

#models.Base.metadata.create_all(engine) 
@app.on_event("startup")
async def startup_event():
    await arq_worker.start(handle_signals=False)

@app.on_event("shutdown")
async def shutdown_event():
    await arq_worker.close()


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