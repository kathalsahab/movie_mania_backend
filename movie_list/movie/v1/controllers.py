"""Category Management Controller."""
import datetime
from sqlalchemy.exc import SQLAlchemyError
from movie_list.constants import ERROR_IN_EXECUTION_QUERY

from movie_list.design.models import Genre, Movies
from movie_list.utils import (
    MovieAlreadyExists,
    RecordNotFound,
    Response,
    FieldMissing,
)
from movie_list.extensions import db
from ..schema import GenreSchema, movie_list_schema_list


def get_movie_list(args: dict):
    """List all the category with filters

    Args:
        args (dict): pagination and filter information

    Returns:
        list : list of user objects
    """

    title = args["title"]
    genre_id = args["genre_id"]
    try:
        query = Movies.query.filter(Movies.is_active == True)
        if title:
            query = query.filter(Movies.title.like(f"%{title}%"))

        if genre_id:
            query = query.filter(Movies.genre_id == genre_id)

    except Exception as exc:
        return Response.failure(400, ERROR_IN_EXECUTION_QUERY, payload=str(exc))

    return Response.success(data=movie_list_schema_list.dump(query))


def delete_movie(movie_id: int):
    """Delete an existing category

    Args:
        category_id (int): id of the user to be deleted

    Returns:
        str : Status of deletion
    """
    try:
        movie = Movies.query.filter(Movies.movie_id == movie_id).first()

        if not movie:
            raise RecordNotFound

        db.session.query(Movies).filter(Movies.movie_id == movie_id).update(
            {Movies.is_active: False}
        )
        db.session.commit()

        return Response.success("Category deleted successfully"), 204
    except RecordNotFound as re:
        return Response.failure(400, "Category does not exist", payload=str(re))
    except SQLAlchemyError as exc:
        return Response.failure(500, f"Error while submitting data", payload=str(exc))
    except Exception as exc:
        return Response.failure(500, "Failed to delete category", payload=str(exc))


def create_new_movie(request_json):
    try:
        movie = Movies.create_movie(
            title=request_json["title"],
            release_date=request_json.get("release_date"),
            genre_id=request_json["genre_id"],
            price=request_json["price"],
            rating=request_json["rating"],
        )
        if not movie:
            raise MovieAlreadyExists

        return (
            Response.success(msg="New Movies Created"),
            201,
        )

    except RecordNotFound as re:
        return Response.success(data=[], msg=re)
    except MovieAlreadyExists as mae:
        return Response.failure(error_code=400, payload=str(mae))
    except FieldMissing as exc:
        return Response.failure(
            error_code=400,
            msg="Required field in request does not exist!",
            payload=str(exc),
        )
    except SQLAlchemyError as exc:
        return Response.failure(
            error_code=400, msg="Error in execution of database query", payload=str(exc)
        )
    except Exception as exc:
        Response.failure(500, payload=str(exc))


def update_movie(args):
    try:
        movie_id = args["movie_id"]
        old_movie = Movies.query.filter_by(movie_id=movie_id, is_active=True).first()
        if not old_movie:
            raise RecordNotFound

        Movies.update_movie(
            movie_id=args["movie_id"],
            title=args["title"],
            release_date=args.get("release_date"),
            genre_id=args["genre_id"],
            price=args["price"],
            rating=args["rating"],
        )

        return Response.success(msg="Category updated succesfully."), 204

    except RecordNotFound as re:
        return Response.failure(error_code=400, payload=str(re))
    except SQLAlchemyError as exc:
        return Response.failure(500, f"Error while submitting data", payload=str(exc))
    except Exception as exc:
        return Response.failure(500, payload=str(exc))


def get_all_genre():
    try:
        return Response.success(GenreSchema(many=True).dump(Genre.query))
    except SQLAlchemyError as exc:
        return Response.failure(500, f"Error while submitting data", payload=str(exc))
    except Exception as exc:
        return Response.failure(500, payload=str(exc))
