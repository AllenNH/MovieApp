from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from datetime import datetime


def get_location_by_name(db : Session, location_name : str):
    return db.query(models.Location).filter(models.Location.name == location_name).first()


def get_location_by_id(db : Session, Location_id : int):
    return db.query(models.Location).filter(models.Location.id == Location_id).first()


def create(request : schemas.location, db : Session ):
    new_location = models.Location(name=request.name,
                    state = request.state,
                    pincode=request.pincode,)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


def get_all_location(db: Session):
    location = db.query(models.Location).all()
    return location

def update(id: int, request: schemas.location, db: Session):
    location = db.query(models.Location).filter(models.Location.id == id)
    if not location.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {id} not found")
    location_exist = db.query(models.Location).filter(models.Location.pincode 
                                        == request.pincode)
    if  location_exist.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Location with pincode {request.pincode} already present")
    location.update(request.dict())
    db.commit()
    return 'updated'

def destroy(id: int,db: Session):
    location = db.query(models.Location).filter(
            models.Location.id == id)
    if not location.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Location with {id} is not available")
    location.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'