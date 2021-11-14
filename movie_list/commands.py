import logging
from flask.cli import AppGroup, with_appcontext
from movie_list.commands_seed_data import create_genre_data

from movie_list.extensions import db


movie_list_cli = AppGroup("movie_list", help="movie_list custom CLI commands")


@movie_list_cli.command(name="create_database")
def create_database():
    """Create SQL database tables, if not created already."""
    db.create_all()


@movie_list_cli.command(name="deploy")
@with_appcontext
def deploy():
    """deploy command used create all necessary tables\
         and insert necessary entries while starting the application.
    """

    # Create Database
    db.create_all()

    # Seed fill genre table
    create_genre_data()
