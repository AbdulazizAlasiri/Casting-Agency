import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor ,setup_db,db_drop_and_create_all
from auth import AuthError, requires_auth
import json

# PER_PAGE=10

# def paginate_question(request, selection):
#     page = request.args.get('page', 1, type=int)
#     start = (page - 1) * PER_PAGE
#     end = start + PER_PAGE

#     questions = [question.format() for question in selection]
#     current_questions = questions[start:end]

#     return current_questions


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    db_drop_and_create_all()

    '''
    actors 
    '''
    
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        actors_selection=Actor.query.order_by('id').all()
        actors=[actor.format() for actor in actors_selection]

        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors':len(actors_selection)
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(paylode):
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if not name :
            abort(400)
        try:
            actor = Actor(name=name, age=age,gender=gender)

            actor.insert()

            formated_actor = [actor.format()]
            return jsonify({
                'success': True,
                'drinks': formated_actor
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
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')
            actor.update()

            formated_actor = [actor.format()]
            return jsonify({
                'success': True,
                'drinks': formated_actor
            })

        except:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(paylode, actor_id):

        drink = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            })

        except:
            abort(400)
    '''
    movies
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        movies_selection=Movie.query.order_by('id').all()
        movies=[movie.format() for movie in movies_selection]

        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies':len(movies_selection)
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
                'drinks': formated_movie
            })
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(paylode, movie_id):
        body = request.get_json()
        if not body:
            abort(400)

        movie = Movie.query.filter(Movie.id == movies_id).one_or_none()
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
                'drinks': formated_movie
            })

        except:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(paylode, movie_id):

        drink = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            })

        except:
            abort(400)


    # @app.route('/')
    # def get_greeting():
    #     excited = os.environ['EXCITED']
    #     greeting = "Hello" 
    #     if excited == 'true': greeting = greeting + "!!!!!"
    #     return greeting

    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

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


if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)