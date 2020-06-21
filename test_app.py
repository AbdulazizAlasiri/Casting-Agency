# test casting-agency localy if you want to test it in prodaction use postman

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

    # database_path=os.environ['DATABASE_URL']

    # this function to add some values to the test database

    def insert_data(self):
        """Seed test database with initial data"""
        actor1 = Actor(name="Actor One", birth_year=2001, gender='m')
        actor2 = Actor(name="Actor Two", birth_year=2002, gender='f')
        actor3 = Actor(name="Actor Three", birth_year=2003, gender='f')

        movie1 = Movie(title="The One", release_date='2001-4-23')
        movie2 = Movie(title="The Two", release_date='2002-4-21')
        movie3 = Movie(title="The Three", release_date='2003-4-23')

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
# SETUP TESTS
# ---------------------------------------------------------------------------------

    def setUp(self):
        """ Configure test client with app & db """
        self.app = create_app()

        self.client = self.app.test_client
        self.prod_headers = {
            "Authorization": "Bearer {}".format(EXEC_PROD_TOKEN)}
        self.dir_headers = {
            "Authorization": "Bearer {}".format(CAST_DIR_TOKEN)}
        self.asst_headers = {
            "Authorization": "Bearer {}".format(CAST_ASST_TOKEN)}

        'Test localy'

        self.database_name = "test"
        self.password = "12"
        self.database_path = "postgres://postgres:{}@{}/{}".format(self.password,
                                                                   'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()

            # remove the folowing three lines if you want to test on existing database
            self.db.drop_all()
            self.db.create_all()
            self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        pass


# ---------------------------------------------------------------------------------
# ACTORS.
# ---------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------
    # Without headers

    def test_get_actors_with_NO_HEADERS(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_post_actors_with_NO_HEADERS(self):
        res = self.client().post('/actors', json={
            'name': 'Test Actor1',
            'birth_year': 1998,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_patch_actors_with_NO_HEADERS(self):
        res = self.client().patch('/actors/4', json={
            'name': 'Test Actor2',
            'birth_year': 1988,
            'gender': 'f'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_delete_actors_with_NO_HEADERS(self):
        res = self.client().delete('/actors/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')



    # -----------------------------------------------------------------------------
    # Executive Producer role

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
            'name': 'Test Actor3',
            'birth_year': 1998,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers=self.prod_headers, json={
            'name': 'Test Actor4',
            'birth_year': 1999
        })
        body = json.loads(res.data)
        actors = body['actor']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Casting Director role

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
            'birth_year': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers=self.dir_headers, json={
            'name': 'Jane Smith',
            'birth_year': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Casting Assistant role

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
            'birth_year': 34,
            'gender': 'm'
        })

        self.assertEqual(res.status_code, 401)

    def test_patch_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().patch('/actors/2', headers=self.asst_headers, json={
            'name': 'Jane Smith',
            'birth_year': 24,
            'gender': 'f'
        })

        self.assertEqual(res.status_code, 401)

    def test_delete_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/actors/2', headers=self.asst_headers)

        self.assertEqual(res.status_code, 401)


# ---------------------------------------------------------------------------------
# MOVIES
# ---------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Without headers

    def test_get_movies_with_NO_HEADERS(self):
        res = self.client().get('/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_post_movies_with_NO_HEADERS(self):
        res = self.client().post('/movies', json={
            'title': 'Added movie',
            'year': 3030
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_patch_movies_with_NO_HEADERS(self):
        res = self.client().patch('/movies/4', json={
            'title': 'edited movie',
            'year': 3030
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_delete_movies_with_NO_HEADERS(self):
        res = self.client().delete('/movies/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    # -----------------------------------------------------------------------------
    # Executive Producer role

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


    def test_delete_movies(self):
        res = self.client().delete('/movies/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Casting Director role

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

    def test_delete_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/movies/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # -----------------------------------------------------------------------------
    # Casting Assistant role

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

    def test_delete_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/movies/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

# ---------------------------------------------------------------------------------
# MOVIE_ACTORS
# ---------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Without headers

    def test_get_ators_by_movie_with_NO_HEADERS(self):
        res = self.client().get('/movies/2/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_assgin_ators_by_movie_with_NO_HEADERS(self):
        res = self.client().post('/movies/2/actors', json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    def test_remove_ators_by_movie_with_NO_HEADERS(self):
        res = self.client().delete('/movies/2/actors', json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'no_authorization_header')

    # -----------------------------------------------------------------------------
    # Executive Producer role

    def test_get_ators_by_movie(self):
        res = self.client().get(
            '/movies/2/actors', headers=self.prod_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_ators_by_movie(self):
        res = self.client().post('/movies/2/actors', headers=self.prod_headers, json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)


    def test_delete_ators_by_movie(self):
        res = self.client().delete('/movies/2/actors', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Casting Director role

    def test_get_ators_by_movie(self):
        res = self.client().get(
            '/movies/2/actors', headers=self.dir_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_ators_by_movie(self):
        res = self.client().post('/movies/2/actors', headers=self.dir_headers, json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)


    def test_delete_ators_by_movie(self):
        res = self.client().delete('/movies/2/actors', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Casting Assistant role

    def test_get_ators_by_movie(self):
        res = self.client().get(
            '/movies/2/actors', headers=self.asst_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_ators_by_movie(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/movies/2/actors', headers=self.asst_headers, json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    def test_delete_ators_by_movie(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/movies/2/actors', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
