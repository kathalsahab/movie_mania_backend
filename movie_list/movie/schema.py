"""Movie Schema
"""
from marshmallow import fields
from movie_list.extensions import mm
from movie_list.design.models import Genre, Movies


class GenreSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre


class MoviesSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Movies

    price = fields.Float()
    rating = fields.Float()

    genre = fields.Nested(GenreSchema())


movie_list_schema_list = MoviesSchema(many=True)
movie_list_schema_single = MoviesSchema()
