import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_path = os.environ['DATABASE_URL']
database_name = "test"
password='12'
database_path = "postgres://postgres:{}@{}/{}".format(password,
    'localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()





movies_actors = db.Table(
    'movies_actors',
    db.Column('actor_id', db.Integer,
              db.ForeignKey('actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer,
              db.ForeignKey('movies.id'), primary_key=True),
)

'''
Actor

'''


class Actor (db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(String)
    gender = Column(String(1))
    movies = db.relationship('Movie', secondary=movies_actors,
                             backref=db.backref('actors', lazy=True))
    def __init__(self, name, birth_year, gender):
        self.name = name
        self.birth_year = birth_year
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'gender': self.gender,
        }


'''
Movie

'''


class Movie (db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    release_date = db.Column(Date)
    actors = db.relationship('Actor', secondary=movies_actors,
                             backref=db.backref('movies', lazy=True))


    def __init__(self, type):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'title': self.title,
            'release_date': self.release_date
        }
