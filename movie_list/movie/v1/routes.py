from flask.globals import request
from flask_restx import Resource, Namespace, reqparse

from movie_list.utils import check_for_datetime, check_for_rating, check_for_title


from . import controllers as c

api = Namespace(
    "Movie Management",
    description="Endpoints related to Movie management",
)


def movie_create():

    parser = reqparse.RequestParser()

    parser.add_argument("title", type=check_for_title, required=True)
    parser.add_argument("release_date", type=check_for_datetime, required=False)
    parser.add_argument("genre_id", type=int, required=True)
    parser.add_argument("price", type=float, required=False)
    parser.add_argument("rating", type=check_for_rating, required=False)

    return parser


movie_create_params = movie_create()


def movie_update():

    parser = reqparse.RequestParser()

    parser.add_argument("movie_id", type=int, required=True)
    parser.add_argument("title", type=check_for_title, required=False)
    parser.add_argument("release_date", type=check_for_datetime, required=False)
    parser.add_argument("genre_id", type=int, required=False)
    parser.add_argument("price", type=float, required=False)
    parser.add_argument("rating", type=check_for_rating, required=False)

    return parser


movie_update_params = movie_update()


@api.route("/movie", endpoint="movie_management")
class MovieManagement(Resource):
    """Class for movies CRUD operations"""

    def get(self):
        """Get list of all movies with filters"""
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, location="args", default=None)
        parser.add_argument("genre_id", type=int, location="args", default=None)
        args = parser.parse_args()
        return c.get_movie_list(args)

    @api.expect(movie_create_params)
    def post(self):
        """Create a new movie"""
        args = movie_create_params.parse_args()
        return c.create_new_movie(args)


@api.route("/movie/edit", endpoint="movie_edit")
class MovieEditDetails(Resource):
    """Class for movies edit operations"""

    @api.expect(movie_update_params)
    def put(self):

        args = movie_update_params.parse_args()
        return c.update_movie(args)

    def delete(self):
        """Delete an existing movie"""
        parser = reqparse.RequestParser()
        parser.add_argument("movie_id", type=int, location="args", required=True)

        args = parser.parse_args()
        return c.delete_movie(args["movie_id"])


@api.route("/movie/genre", endpoint="movie_genre")
class MovieGenreDetails(Resource):
    """Class for genre list"""

    def get(self):
        return c.get_all_genre()
