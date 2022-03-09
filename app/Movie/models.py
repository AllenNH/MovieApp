from sqlalchemy import Boolean,Float, Column, ForeignKey, Integer, String, DateTime, Time
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
    show = relationship("Show",back_populates="bookings")
    showSeat = relationship("ShowSeat",back_populates="bookings")


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

    show = relationship("Show",back_populates="movie")


class Cinema(Base):
    __tablename__ = "cinema"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    noOfScreens = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    location_id = Column(Integer, ForeignKey('location.id'))

    location = relationship("Location",back_populates="cinema")
    cinemaHall = relationship("CinemaHall",back_populates="cinema")


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    state = Column(String)
    pincode = Column(Integer)

    cinema = relationship("Cinema",back_populates="location")


class CinemaHall(Base):
    __tablename__ = "cinemaHall"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    totalSeats = Column(Integer)
    cinema_id = Column(Integer, ForeignKey('cinema.id'))  

    cinema = relationship("Cinema",back_populates="cinemaHall")
    cinemaSeat = relationship("CinemaSeat",back_populates="cinemaHall")
    show = relationship("Show",back_populates="cinemaHall", uselist=False)

class CinemaSeat(Base):
    __tablename__ = "cinemaSeat"
    id = Column(Integer, primary_key=True, index=True)
    seatNo = Column(String)
    seatType = Column(String)
    flag = Column(Integer, default=1)
    cinemaHall_id = Column(Integer, ForeignKey('cinemaHall.id')) 

    
    cinemaHall = relationship("CinemaHall",back_populates="cinemaSeat")    
    showSeat = relationship("ShowSeat",back_populates="cinemaSeat")

    

    
class Show(Base):
    __tablename__ = "show"
    id = Column(Integer, primary_key=True, autoincrement=True)
    showDate = Column(DateTime)
    startTime = Column(Time)
    endTime = Column(Time)
    cinemaHall_id = Column(Integer, ForeignKey('cinemaHall.id'))
    movie_id = Column(Integer, ForeignKey('movie.id'))

    bookings = relationship('Booking', back_populates="show")
    movie = relationship("Movie",back_populates="show")
    cinemaHall = relationship("CinemaHall",back_populates="show")
    showSeat = relationship("ShowSeat",back_populates="show")


class ShowSeat(Base):
    __tablename__ = "showSeat"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean)
    price = Column(Float)
    cinemaSeat_id = Column(Integer, ForeignKey('cinemaSeat.id'))
    show_id = Column(Integer, ForeignKey('show.id'))
    booking_id = Column(Integer, ForeignKey('booking.id'))

    bookings = relationship('Booking', back_populates="showSeat")
    cinemaSeat = relationship("CinemaSeat",back_populates="showSeat")
    show = relationship("Show",back_populates="showSeat")





