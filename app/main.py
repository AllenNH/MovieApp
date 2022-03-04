from fastapi import FastAPI, Depends
from Movie import schemas, models, database
from Movie.database import  engine
from sqlalchemy.orm import Session
from Movie.routers import user, authenticate_user
app = FastAPI()

models.Base.metadata.create_all(engine) 


app.include_router(authenticate_user.router)
app.include_router(user.router)
