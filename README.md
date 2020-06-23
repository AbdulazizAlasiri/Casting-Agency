# Full Stack Trivia API Backend

## Introduction

Casting-Agency is the fifth and the final project in Udacity nanodgree. It models a company that is responsible for creating movies and managing and assigning actors to those movies. The user can intract with the database useing the API to prform CRUD .The user must have permissions to prform these oparation.the permissions are manged by [Auth0](https://auth0.com/).

The API is doploued in [Heroku](https://dashboard.heroku.com/) in the folowing base URL :

```bash
https://casting-agency-fsnd-project.herokuapp.com/
```

## Getting Started

If you want to run the API localy, folow the instraction.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/fsnd-capstone` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

If you want to use tha API localy .

1. With postgres runing , Create a database with any name.
2. Uncomment line 9 to 12 in models.py
3. Modify the database name and the password to your database name and password
4. Uncomment line 53 and 54 in app.py to create the tables and insert some data to the database

## Running the server

From within the `fsnd-capstone` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source  setup.sh
python app.py
```

setup.sh have the variable needed to run and test the app.

## Testing

you can test the endpoint using Unittest or Postman.

### Unittest

tests for the endpoint are in test_app.py

first you neeed to create a database and name it 'test'
To run the tests, run

```
python test_app.py
```

### Postman

To test the endpoint in [Heroku](https://dashboard.heroku.com/) :

1. download [Postmant](https://www.postman.com/).
2. Import Casting-Agency.postman_collection.json .
3. run the collection.

## API Reference

### Geting Starting

Base URL:this app can be run locally using the base URL as http://127.0.0.1:5000/,or you can use hosted URL https://casting-agency-fsnd-project.herokuapp.com .
Authentication: This version of the application does not have frontend to authnticate users , to use the endpoints you need to provaied a valid Bearer access token,given in setup.sh or by using the folowing token :

```bash
Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilk2QkJaZUtXUVdYMklSY2xudy1xUyJ9.eyJpc3MiOiJodHRwczovL2FiZHVsYXppei5hdXRoMC5jb20vIiwic3ViIjoiMkJFS29hVzlKY0lsNllxbDFWZ0ZYNm52V3JtcDk0Q1FAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTkyNTk4MzI3LCJleHAiOjE1OTM0NjIzMjcsImF6cCI6IjJCRUtvYVc5SmNJbDZZcWwxVmdGWDZudldybXA5NENRIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgcG9zdDphY3RvcnMgcG9zdDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBkZWxldGU6bW92aWVzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgYXNzaWduOmFjdG9ycyByZW1vdmU6YWN0b3JzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJhc3NpZ246YWN0b3JzIiwicmVtb3ZlOmFjdG9ycyJdfQ.E1vnj_zWoMLEHgbLx3bJFP7LgzB7kLnvH__FZ-LcFAIsoMLgoWVmZnw3QRVl6nQreiqHFk5TaWGSuzAfpmFtFtz7WliSL7yXTzT1T1_SNurbTyPVJLG1TU4VV-8oUcUr5j-0g8VkVklJqDtsGbLrZIteAU9preg4qMuJGkM2v3MahKcpyklVLmO3agKhgo2-P-LtHXASe4OzxpVCd1NZ4ARY7pxPYMwC5KbCIuP4lnMuUMT0fFi0ANXcnIzbwaTM7uq9VOvSik8CY62d4XXL5fGLxljjcway9kP0JsG3xjw4Z8PeWhucnkGVF52rSfDPpkhVRIGTLyxQbQcK8XXy2g
```

### Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
"success": False,
"error": 400,
"message": "bad request"
}
```

The API will return three error types when requests fail:

400: Bad Request
401: Unauthorized
404: Resource Not Found
405: Method Not Allowed
422: Not Processable

500: Internal Server Error

### End Points

The folowing tests will assume that the access token is porvided with each requaset body in the form:

```bash
"Authorization": "Bearer {access_token}".
```

#### Actors

GET /actors
General:
Returns a list of actors objects , success value and the number of actors
Sample: curl https://casting-agency-fsnd-project.herokuapp.com/actors

```bash
{
    "actors": [
        {
            "birth_year": "2001",
            "gender": "m",
            "id": 1,
            "name": "Actor One"
        },
        {
            "birth_year": "2002",
            "gender": "f",
            "id": 2,
            "name": "Actor Two"
        },
        {
            "birth_year": "2003",
            "gender": "f",
            "id": 3,
            "name": "Actor Three"
        }
    ],
    "success": true,
    "total_actors": 3
}
```

POST /actors
General:
Creates a new actor using the provided name, birth_year and gender. Returns an array contans the actor created and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d '{
"name": "Added Actor",
"birth_year": 100,
"gender": "m"
}'

```bash
{
    "actors": [
        {
            "birth_year": "100",
            "gender": "m",
            "id": 6,
            "name": "Added Actor"
        }
    ],
    "success": true
}

```

PATCH /actors/{int:actor_id}
General:
modify the actor with the id = actor_id using the provided name, birth_year or gender. Returns an array contans the actor modified and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/actors/5 -X PATCH -H "Content-Type: application/json" -d '{
"name": "Edited Actor",
"gender": "m"
}'

```bash
{
    "actors": [
        {
            "birth_year": "200",
            "gender": "f",
            "id": 5,
            "name": "edited actor"
        }
    ],
    "success": true
}

```

DELETE /actors/{int:actor_id}
General:
Deletes the actors with the provided ID .Returns an array contans the actor and success value.
curl https://casting-agency-fsnd-project.herokuapp.com//movies/5 -X DELETE -H "Content-Type: application/json"

```bash
{
    "deleted": [
        {
            "birth_year": "200",
            "gender": "f",
            "id": 5,
            "name": "edited actor"
        }
    ],
    "success": true
}
```

#### Movie

GET /movie
General:
Returns a list of movie objects , success value and the number of movies
Sample: curl https://casting-agency-fsnd-project.herokuapp.com/movies

```bash
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 23 Apr 2001 00:00:00 GMT",
            "title": "The One"
        },
        {
            "id": 2,
            "release_date": "Sun, 21 Apr 2002 00:00:00 GMT",
            "title": "The Two"
        },
        {
            "id": 3,
            "release_date": "Wed, 23 Apr 2003 00:00:00 GMT",
            "title": "The Three"
        }
    ],
    "success": true,
    "total_movies": 3
}
```

POST /movies
General:
Creates a new actor using the provided name, birth_year and gender. Returns an array contans the actor created and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/movies -X POST -H "Content-Type: application/json" -d '{
"title": "added movie",
"release_date": "2000-01-20"
}'

```bash
{
    "movies": [
        {
            "id": 4,
            "release_date": "Thu, 20 Jan 2000 00:00:00 GMT",
            "title": "added movie"
        }
    ],
    "success": true
}

```

PATCH /movies/{int:movie_id}
General:
modify the movie with the id = movie_id using the provided release_date or title. Returns an array contans the movie modified and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/movies/4 -X PATCH -H "Content-Type: application/json" -d '{
"title": "edited movie",
"release_date": "3000-02-01"
}'

```bash
{
    "movies": [
        {
            "id": 4,
            "release_date": "Sat, 01 Feb 3000 00:00:00 GMT",
            "title": "edited movie"
        }
    ],
    "success": true
}

```

DELETE /movies/{int:movie_id}
General:
Deletes the movie with the provided ID .Returns an array contans the movie and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/movie/4 -X DELETE -H "Content-Type: application/json"

```bash
{
    "deleted": [
        {
            "id": 4,
            "release_date": "Sat, 01 Feb 3000 00:00:00 GMT",
            "title": "edited movie"
        }
    ],
    "success": true
}
```

#### Actors in a Movie

GET /movies/{int:movie_id}/actors
General:
Returns a list of actors objects assgined to a movie with id = to movie_id, success value and the number of actors
Sample: curl https://casting-agency-fsnd-project.herokuapp.com/movies/2/actors

```bash
{
    "actors": [
        {
            "birth_year": "2003",
            "gender": "f",
            "id": 3,
            "name": "Actor Three"
        }
    ],
    "success": true,
    "total_actors": 1
}
```

POST /movies/{int:movie_id}/actors
General:
assgin the actor with the id provided to the movie with the id = movie_id . Returns an array contans the actor assgined and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/movies/2/actors -X POST -H "Content-Type: application/json" -d '{
"actor_id": "1"
}'

```bash
{
    "actors": [
        {
            "birth_year": "2001",
            "gender": "m",
            "id": 1,
            "name": "Actor One"
        }
    ],
    "success": true
}

```

DELETE /movies/{int:movie_id}/actors
General:
remove the actor with the id provided from working in the movie with the id = movie_id . Returns an array contans the actor removed and success value.
curl https://casting-agency-fsnd-project.herokuapp.com/movies/2/actors -X DELETE -H "Content-Type: application/json" -d '{
"actor_id": "1"
}'

```bash
{
    "actors": [
        {
            "birth_year": "2001",
            "gender": "m",
            "id": 1,
            "name": "Actor One"
        }
    ],
    "success": true
}

```

## Authors

[AbdulazizAlasiri](https://github.com/AbdulazizAlasiri)
