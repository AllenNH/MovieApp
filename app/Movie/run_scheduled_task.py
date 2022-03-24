from . import schemas, models
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///../movie1.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, 
                                autoflush=False, bind=engine)


session = SessionLocal()


def clear_old_movie():
    shows  = session .query(models.Show).\
        filter(models.Show.status == True, 
                    func.date(models.Show.showDate) < date.today()).all()
    for show in shows:
        show.status = False
    session.commit()
    print("scheduled_task ->show updated")
