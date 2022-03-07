from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database
from sqlalchemy.orm import Session
from Movie.repository import movie
from typing import List 


get_db = database.get_db
router = APIRouter(
    prefix = '/movie',
    tags = ['Movie']

)


@router.post('/add_movie')
def create(request : schemas.movie , db : Session = Depends(get_db)):
    db_movies = movie.get_movie_by_name(db, request.title)
    print(db_movies)
    if db_movies:
        raise HTTPException(status_code=400, 
                detail=f"Movie with name{request.title} already exists")
    return movie.create(request, db)


@router.get('/movie_details',status_code=200,
            response_model=List[schemas.showMovie])
def get_all_movie(db : Session = Depends(get_db)):
    return movie.get_all_movie(db)


@router.put('/{title}', status_code=202)
def update(title,request : schemas.movie, db : Session = Depends(get_db)):
    return movie.update(title,request,db)


@router.delete('/{title}', status_code=status.HTTP_200_OK)
def destroy(title, db : Session = Depends(get_db)):
    return movie.destroy(title,db)


