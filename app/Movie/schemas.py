from typing import List, Optional
from pydantic import BaseModel

class user(BaseModel):
    
    name : str
    phone : int 
    password : str


class ShowUser(BaseModel):
    id : int
    phone : int
    name : str
    
    class Config():
        orm_mode = True
    

class TokenData(BaseModel):
    id : Optional[int] = None
    role : Optional[str] = None
    name: Optional[str] = None


class cinema(BaseModel):

    name : str 
    noOfScreens : int


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