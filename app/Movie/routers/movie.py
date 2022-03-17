from fastapi import APIRouter, Depends, HTTPException, status
from Movie import schemas, database, oauth2
from sqlalchemy.orm import Session
from Movie.repository import movie
from typing import List, Optional 


get_db = database.get_db
router = APIRouter(
    prefix = '/movie',
    tags = ['Movie']

)


@router.post('/add_movie')
def create(request : schemas.movie , db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    db_movies = movie.get_movie_by_name(db, request.title)
    print(db_movies)
    if db_movies:
        raise HTTPException(status_code=400, 
                detail=f"Movie with name{request.title} already exists")
    return movie.create(request, db, current_user.id)

@router.get('/get_current_movies',status_code=200,
            response_model=List[schemas.showMovie])
def get_current_movies(db : Session = Depends(get_db)):
    return movie.get_all_current_movie(db)

@router.get('/get_current_movies/{location}',status_code=200,
            response_model=List[schemas.showMovie])
def get_current_movies_by_location(location: str, db : Session = Depends(get_db)):
    return movie.get_all_current_movie_by_location(db, location)


@router.get('/movie_details',status_code=200,
            response_model=List[schemas.showMovie])
def get_all_movie(db : Session = Depends(get_db)):
    return movie.get_all_movie(db)

@router.get('/movie_details/{title}', status_code=200)
def get_movie_by_title(title: str, db : Session = Depends(get_db)):
    return movie.get_movie_by_name(db,title)

@router.put('/edit/{title}', status_code=202)
def update(title,request : schemas.movie, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return movie.update(title, request, db, current_user.id)


@router.delete('/delete/{title}', status_code=status.HTTP_200_OK)
def destroy(title, db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    return movie.destroy(title,db)

@router.get('/Search')
def search_movie(name : Optional[str] = None,  db : Session = Depends(get_db) ):
    return movie.get_movie_by_name(db,name)

@router.put('/change_status/{id}', status_code=202)
def change_status(id: int,status: bool,db : Session = Depends(get_db),
        current_user: schemas.user = Depends(oauth2.check_if_admin)):
    
    return movie.change_status(id,status,db)