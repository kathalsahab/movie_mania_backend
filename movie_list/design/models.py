"""Centralised location for all the DB Models
"""
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

# Third party imports
from sqlalchemy import (
    Integer,
    Column,
    DateTime,
    String,
)
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL, Boolean

# Application imports
from movie_list.extensions import db
from movie_list.utils import RecordNotFound
from sqlalchemy.types import String


class Genre(db.Model):
    __tablename__ = "genre"

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(255), nullable=False)

    @classmethod
    def lookup(cls, genre_name):
        return cls.query.filter_by(genre_name=genre_name).first()

    @staticmethod
    def create_genre(genre_name):
        genre = Genre.lookup(genre_name)
        if genre:
            return

        genre = Genre()
        genre.genre_name = genre_name

        db.session.add(genre)
        db.session.commit()
        return genre


class Movies(db.Model):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    release_date = Column(DateTime)
    price = Column(DECIMAL(10, 5))
    rating = Column(DECIMAL(10, 5))
    is_active = Column(Boolean, default=True)
    genre_id = Column(Integer, ForeignKey(Genre.genre_id), nullable=False)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    genre = relationship("Genre", backref="movie", lazy=True)

    @classmethod
    def lookup(cls, title):
        return cls.query.filter_by(title=title).first()

    @property
    def genre_name(self):
        return self.genre.genre_name

    @staticmethod
    def create_movie(title, release_date, genre_id, price=None, rating=None):
        movie = Movies.query.filter_by(title=title, is_active=True).first()
        if movie:
            return
        movie = Movies()
        movie.title = title
        if release_date:
            movie.release_date = release_date
        movie.genre_id = genre_id
        if price:
            movie.price = price
        if rating:
            movie.rating = rating
        db.session.add(movie)
        db.session.commit()
        return movie

    @staticmethod
    def update_movie(movie_id, title, release_date, genre_id, price=None, rating=None):
        movie = Movies.query.filter_by(movie_id=movie_id, is_active=True).first()
        if not movie:
            raise RecordNotFound
        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date
        if genre_id:
            movie.genre_id = genre_id
        if price:
            movie.price = price
        if rating:
            movie.rating = rating
        db.session.add(movie)
        db.session.commit()
        return movie
