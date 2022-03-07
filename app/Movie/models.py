from turtle import title
from sqlalchemy import Boolean,Float, Column, ForeignKey, Integer, String, DateTime
from Movie.database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(Integer, unique=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default='user')
    timestamp = Column(DateTime)

    bookings = relationship('Booking', back_populates="users")


class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    noOfseats = Column(Integer)
    timestamp = Column(DateTime)
    status = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    show_id = Column(Integer, ForeignKey('show.id'))

    users = relationship('User', back_populates="bookings")


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    duration = Column(Integer)
    language = Column(String)
    genre = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))


class Cinema(Base):
    __tablename__ = "cinema"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    noOfScreens = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    location_id = Column(Integer, ForeignKey('location.id'))


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    state = Column(String)
    pincode = Column(Integer)


class CinemaHall(Base):
    __tablename__ = "cinemaHall"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    totalSeats = Column(Integer)
    cinema_id = Column(Integer, ForeignKey('cinema.id'))  

class CinemaSeat(Base):
    __tablename__ = "cinemaSeat"
    id = Column(Integer, primary_key=True, index=True)
    seatNo = Column(String)
    seatType = Column(Integer)
    cinemaHall_id = Column(Integer, ForeignKey('cinemaHall.id')) 

    
class Show(Base):
    __tablename__ = "show"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    cinemaHall_id = Column(Integer, ForeignKey('cinemaHall.id'))
    movie_id = Column(Integer, ForeignKey('movie.id'))


class ShowSeat(Base):
    __tablename__ = "showSeat"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean)
    price = Column(Float)
    cinemaSeat_id = Column(Integer, ForeignKey('cinemaSeat.id'))
    show_id = Column(Integer, ForeignKey('show.id'))
    booking_id = Column(Integer, ForeignKey('booking.id'))





