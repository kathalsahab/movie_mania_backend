from movie_list.extensions import db
from movie_list.utils import Response


def handle_ping():
    return Response.success("Pong")
