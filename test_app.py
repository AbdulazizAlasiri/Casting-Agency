
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from flask import jsonify


EXEC_PROD_TOKEN = os.environ['EXEC_PROD_TOKEN']
CAST_DIR_TOKEN = os.environ['CAST_DIR_TOKEN']
CAST_ASST_TOKEN = os.environ['CAST_ASST_TOKEN']

class CastingAgencyCase(unittest.TestCase):

    'Test localy'

    database_name = "test"
    password = "12"
    database_path = "postgres://postgres:{}@{}/{}".format(password,
                                                                'localhost:5432', database_name)
    # database_path=os.environ['DATABASE_URL']

    def insert_data(self):
        """Seed test database with initial data"""
        actor1 = Actor(name="Actor One", age=2001, gender='m')
        actor2 = Actor(name="Actor Two", age=2002, gender='f')
        actor3 = Actor(name="Actor Three", age=2003, gender='f')

        movie1 = Movie(title="Movie One", release_date=2011)
        movie2 = Movie(title="The Two", release_date=2012)
        movie3 = Movie(title="The Three", release_date=2013)

        movie1.actors.append(actor1)
        movie1.actors.append(actor2)
        movie2.actors.append(actor3)

        self.db.session.add(actor1)
        self.db.session.add(actor2)
        self.db.session.add(actor3)

        self.db.session.add(movie1)
        self.db.session.add(movie2)
        self.db.session.add(movie3)
        self.db.session.commit()
        self.db.session.close()

        



# ---------------------------------------------------------------------------------
# ------------------------------ SETUP TESTS --------------------------------------
# ---------------------------------------------------------------------------------

    def setUp(self):
        """ Configure test client with app & db """
        self.app = create_app()

        self.client = self.app.test_client
        self.prod_headers = {"Authorization": "Bearer {}".format(EXEC_PROD_TOKEN)}
        self.dir_headers = {"Authorization": "Bearer {}".format(CAST_DIR_TOKEN)}
        self.asst_headers = {"Authorization": "Bearer {}".format(CAST_ASST_TOKEN)}


        setup_db(self.app, database_path=database_path)
        # setup_db(self.app, database_path=prod_test_database_path)

        with self.app.app_context():
            self.db = db

            self.db.drop_all()
            self.db.create_all()

            self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        self.db.session.rollback()
        self.db.drop_all()
        self.db.session.close()
        pass

# ---------------------------------------------------------------------------------
# --------------------------------- TEST DB ---------------------------------------
# ---------------------------------------------------------------------------------

    def test_seed_testdb(self):
        """Test Seed Data in Db"""
        actors = Actor.query.all()  # check of actors is a list of Actors
        self.assertEqual(isinstance(actors, list), True)
        self.assertEqual(isinstance(actors[0], Actor), True)
        movies = Movie.query.all()  # check of movies is a list of Movies
        self.assertEqual(isinstance(movies, list), True)
        self.assertEqual(isinstance(movies[0], Movie), True)

# ---------------------------------------------------------------------------------
# ------------------------ UNAUTHENTICATED ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors_with_NO_HEADERS(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_post_actors_with_NO_HEADERS(self):
        res = self.client().post('/actors', json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_patch_actors_with_NO_HEADERS(self):
        res = self.client().patch('/actors/4', json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_get_actors_with_NO_HEADERS(self):
        res = self.client().get('/actors/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_delete_actors_with_NO_HEADERS(self):
        res = self.client().delete('/actors/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')


# ---------------------------------------------------------------------------------
# ------------------------------- PRODUCER ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.prod_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_actors(self):
        res = self.client().post('/actors', headers=self.prod_headers, json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers=self.prod_headers, json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_get_actors(self):
        res = self.client().get('/actors/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

# ---------------------------------------------------------------------------------
# ------------------------------- DIRECTOR ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.dir_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_actors(self):
        res = self.client().post('/actors', headers=self.dir_headers, json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers=self.dir_headers, json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_get_actors(self):
        res = self.client().get('/actors/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)



# ---------------------------------------------------------------------------------
# ------------------------------ ASSISTANT ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.asst_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/actors', headers=self.asst_headers, json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })

        self.assertEqual(res.status_code, 401)

    def test_patch_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().patch('/actors/2', headers=self.asst_headers, json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })

        self.assertEqual(res.status_code, 401)

    def test_get_actors(self):
        res = self.client().get('/actors/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/actors/2', headers=self.asst_headers)

        self.assertEqual(res.status_code, 401)


# ---------------------------------------------------------------------------------
# --------------------------- UNAUTHENTICATED MOVIES ------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies_with_NO_HEADERS(self):
        res = self.client().get('/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_post_movies_with_NO_HEADERS(self):
        res = self.client().post('/movies', json={
            'title': 'The Movie 4',
            'year': 2017
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_patch_movies_with_NO_HEADERS(self):
        res = self.client().patch('/movies/4', json={
            'title': 'The Movie 4',
            'year': 2018
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_get_movies_with_NO_HEADERS(self):
        res = self.client().get('/movies/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_delete_movies_with_NO_HEADERS(self):
        res = self.client().delete('/movies/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

# ---------------------------------------------------------------------------------
# ------------------------------- PRODUCER MOVIES ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.prod_headers)

        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        res = self.client().post('/movies', headers=self.prod_headers, json={
            'title': 'The Movie 4',
            'year': 2017
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_movies(self):
        res = self.client().patch('/movies/2', headers=self.prod_headers, json={
            'title': 'The Movie 4',
            'year': 2018
        })
        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_get_movies(self):
        res = self.client().get('/movies/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_movies(self):
        res = self.client().delete('/movies/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

# ---------------------------------------------------------------------------------
# ------------------------------- DIRECTOR MOVIES ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.dir_headers)

        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/movies', headers=self.dir_headers, json={
            'title': 'The Movie 4',
            'year': 2017
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_patch_movies(self):
        res = self.client().patch('/movies/2', headers=self.dir_headers, json={
            'title': 'The Movie 4',
            'year': 2018
        })
        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_get_movies(self):
        res = self.client().get('/movies/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/movies/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

# ---------------------------------------------------------------------------------
# ------------------------------ ASSISTANT MOVIES ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.asst_headers)

        body = json.loads(res.data)
        movies = body['movies']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/movies', headers=self.asst_headers, json={
            'title': 'The Movie 4',
            'year': 2017
        })

        self.assertEqual(res.status_code, 401)

    def test_patch_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().patch('/movies/2', headers=self.asst_headers, json={
            'title': 'The Movie 4',
            'year': 2018
        })

        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        res = self.client().get('/movies/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/movies/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
