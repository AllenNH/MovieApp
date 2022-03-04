from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from Movie.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(Integer, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    

    


