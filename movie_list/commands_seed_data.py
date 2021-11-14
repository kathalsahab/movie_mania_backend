from movie_list.constants import LIST_OF_GENRES
from movie_list.design.models import Genre


def create_genre_data():
    for genre_name in LIST_OF_GENRES:
        if not Genre.lookup(genre_name):
            Genre.create_genre(genre_name=genre_name)
