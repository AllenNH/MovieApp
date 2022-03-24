from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models
from ..hashing import Hash 
from sqlalchemy.orm import Session
from datetime import datetime


def update(id: int, role: int, db : Session):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")
    
    if role == 1:
        user.role = "admin"
    elif role == 2:
        user.role = "merchant"
    elif role == 3:
        user.role = "user"
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invailid role\n1.admin\n2.merchant\n3.user")
    db.commit()
    return user