#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from models import Movie, Actor, setup_db, db_drop_and_create_all, insert_data
from auth import AuthError, requires_auth


#----------------------------------------------------------------------------#
# Global Variables.
#----------------------------------------------------------------------------#

# this value to test that environment variable exist
EXCITED = os.environ['EXCITED']


# OBJECT_PER_PAGE=10


#----------------------------------------------------------------------------#
# Help Functions.
#----------------------------------------------------------------------------#

# def paginate_objects(request, selection):
#     page = request.args.get('page', 1, type=int)
#     start = (page - 1) * OBJECT_PER_PAGE
#     end = start + OBJECT_PER_PAGE

#     objects = [object.format() for object in selection]
#     current_objects = objects[start:end]

#     return current_objects


def create_app(test_config=None):

    #----------------------------------------------------------------------------#
    # Conf.
    #----------------------------------------------------------------------------#
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    db_drop_and_create_all()
    insert_data()

#----------------------------------------------------------------------------#
# Routes.
#----------------------------------------------------------------------------#

    #----------------------------------------------------------------------------#
    # Actors.

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(paylode):
        actors_selection = Actor.query.order_by('id').all()
        formated_actors = [actor.format() for actor in actors_selection]

        return jsonify({
            'success': True,
            'actors': formated_actors,
            'total_actors': len(actors_selection)
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(paylode):
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', None)
        birth_year = body.get('birth_year', None)
        gender = body.get('gender', None)

        if not name:
            abort(400)
        try:
            actor = Actor(name=name, birth_year=birth_year, gender=gender)

            actor.insert()

            formated_actor = [actor.format()]
            return jsonify({
                'success': True,
                'actors': formated_actor
            })
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(paylode, actor_id):
        body = request.get_json()
        if not body:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            if 'name' in body:
                actor.name = body.get('name')
            if 'birth_year' in body:
                actor.birth_year = body.get('birth_year')
            if 'gender' in body:
                actor.gender = body.get('gender')
            actor.update()

            formated_actor = [actor.format()]
            return jsonify({
                'success': True,
                'actors': formated_actor
            })

        except:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(paylode, actor_id):
        print('paylode!!!!!!!!', paylode)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            formated_actor = [actor.format()]
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': formated_actor
            })

        except:
            abort(400)

    # @app.route('/actors/<int:actor_id>/movies', methods=['GET'])
    # @requires_auth('get:movies')
    # def get_movies_by_actor(paylode, actor_id):

    #     actor = Movie.query.filter(Actor.id == actor_id).one_or_none()
    #     if actor is None:
    #         abort(404)

    #     movies=[movie.format() for movie in actor.movies]
    #     try:

    #         return jsonify({
    #             'success': True,
    #             'movies': movies,
    #             'total_actors':len(movies)

    #         })

    #     except:
    #         abort(400)

    #----------------------------------------------------------------------------#
    # Movies.

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(paylode):
        movies_selection = Movie.query.order_by('id').all()
        formated_movies = [movie.format() for movie in movies_selection]

        return jsonify({
            'success': True,
            'movies': formated_movies,
            'total_movies': len(movies_selection)
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(paylode):
        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title or not release_date:
            abort(400)
        try:
            movie = Movie(title=title, release_date=release_date)

            movie.insert()

            formated_movie = [movie.format()]
            return jsonify({
                'success': True,
                'movies': formated_movie
            })
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(paylode, movie_id):
        body = request.get_json()
        if not body:
            abort(400)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()

            formated_movie = [movie.format()]
            return jsonify({
                'success': True,
                'movies': formated_movie
            })

        except:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(paylode, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        formated_movie = [movie.format()]
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': formated_movie
            })

        except:
            abort(400)

    #----------------------------------------------------------------------------#
    # Movie_Actors.

    '''
    Get all actors acting on the movie with the id == movie_id
    '''
    @app.route('/movies/<int:movie_id>/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors_by_movie(paylode, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        formated_actors = [actor.format() for actor in movie.actors]
        try:

            return jsonify({
                'success': True,
                'actors': formated_actors,
                'total_actors': len(formated_actors)
            })

        except:
            abort(400)

    '''
    Assgin actor with the id provided in the body to the movie with id == movie_id
    '''
    @app.route('/movies/<int:movie_id>/actors', methods=['POST'])
    @requires_auth('assign:actors')
    def add_actors_to_movie(paylode, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        actor_id = body.get('actor_id', None)

        if not actor_id:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.actors.append(actor)
            movie.update()
            formated_actor = [actor.format()]
            return jsonify({
                'success': True,
                'actors': formated_actor,
            })

        except:
            abort(400)

    '''
    Remove actor with the id provided in the body from the movie with id == movie_id
    '''
    @app.route('/movies/<int:movie_id>/actors', methods=['DELETE'])
    @requires_auth('remove:actors')
    def remove_actors_from_movie(paylode, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        actor_id = body.get('actor_id', None)

        if not actor_id:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.actors.remove(actor)
            movie.update()
            formated_actor = [actor.format()]
            return jsonify({
                'success': True,
                'actors': formated_actor,
            })

        except:
            abort(400)

    '''
    this endpoint was made to test that environment variable exist 

    '''
    @app.route('/')
    def get_greeting():

        greeting = "Hello"
        if EXCITED == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    '''
    this endpoint was made for the reviewer.
    it will drop and create all tables and insert some data
    '''
    @app.route('/setup-database')
    def setup_database():

        db_drop_and_create_all()
        insert_data()

        return jsonify({
            'success': True,
        })

#----------------------------------------------------------------------------#
# Errors.
#----------------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error["code"]
        }), AuthError.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)
