# MovieApp

##Problem Statement:
Build an application backend (APIs) to allow booking of movie tickets.
- There can be theatres which will register with your application
- Each Theatre may have multiple "movies" playing in a day
- Each theatre has multiple seats, each seat identified by a unique 2D code (A-4, B-6 etc)
- Customers register with either phone number of mobile
- Booking can be done against a movie in a theatre against a specific seat on a specific date and time slot



##Steps to run API
pwd ->MovieApp
1.pip install -r requirements.txt
2.cd app
3.unicorn main:app --reload
4.connect to localhost/docs (http://127.0.0.1:8000/docs)

currently 3 users are configured:
username: 1 -> admin
          2 -> merchant
          5 -> user
          
password-> admin (for all)
