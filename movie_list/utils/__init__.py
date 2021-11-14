"""Generic Utility Functions
"""
from typing import Union
import re
import datetime
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
    Unauthorized,
    Forbidden,
    InternalServerError,
    Conflict,
)
from flask_restx import abort


DESCENDING_VALUES = ["desc", "DESC", -1, "des", "DES", "D", "d"]


class Response:
    """Generic Response class to envelope the API response."""

    @staticmethod
    def success(
        data: Union[dict, list, str] = None,
        msg=None,
        pagination: dict = None,
        links: dict = None,
        metadata: dict = None,
    ) -> dict:
        """Construct a Enveloped Success response in JSON format.

        Args:
            data (Union[dict, list, str], optional): actual data to send.\
                If None, adds `{}` to response. Defaults to None.

            pagination (dict, optional): Already constructed Pagination dictionary, \
                for List Response. If None, not added to response. Defaults to None.

            links (dict, optional): Already constructed links dictionary \
                for Paginated Response. Defaults to None.

        Returns:
            dict: Complete Enveloped success response object.

        ```py
            {
                "data": {},
                "success": true,
                "metadata":{},
                "pagination":{}
            }
        ```
        """
        _resp = {"data": data if data is not None else {}, "success": True}

        # conditionally add msg
        if msg is not None:
            _resp["message"] = msg
        else:
            if isinstance(data, str):
                _resp["message"] = data

        # conditionally add pagination
        if pagination is not None:
            _resp["pagination"] = pagination

        # conditionally add links
        if links is not None:
            _resp["links"] = links

        # conditionally add meta_data
        if metadata is not None:
            _resp["metadata"] = metadata
        return _resp

    @staticmethod
    def failure(error_code=500, msg=None, payload=None):
        """Construct a Enveloped Failure response in JSON format

        Args:
            error_code (int, optional): Http error codes. Defaults to 500.
            msg (str, optional): Desciption of the error. Defaults to None.
            payload (Union[dict, list, str], optional): Ant extra payload with the error message. Defaults to None.

        Returns:
            dict : Enveloped Failure response in JSON

        ```py
            {
                "error": {
                    "message" : "Error"
                    "payload" : {}
                },
                "success": False
            }
        ```
        """
        if msg is None:
            msg = Response.get_default_message(error_code)
        data = {"message": msg, "payload": payload}
        return abort(error_code, None, error=data, success=False)

    @staticmethod
    def get_default_message(error_code):
        """Get the default error message if not provided.

        Args:
            error_code (int): Http error code.

        Returns:
            str: Default error message or "Error"
        """
        error_msg = {
            "400": BadRequest.description,
            "404": NotFound.description,
            "401": Unauthorized.description,
            "500": InternalServerError.description,
            "403": Forbidden.description,
            "409": Conflict.description,
        }
        return error_msg.get(str(error_code)) or "Error"


def check_for_string(data):
    if not isinstance(data, str):
        raise ValueError("Must be string")
    return data


def check_for_title(data):
    # Must be a string
    check_for_string(data)
    len_data = len(data)
    if len_data < 3 or len_data > 60:
        raise ValueError("String length must be between 3 - 60")
    return data


def check_for_rating(data):
    if float(data) < 0 or float(data) > 10:
        raise ValueError("Decimal value must be between 0-10")
    return data


def check_for_datetime(date):
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").date()
    except Exception as exc:
        raise ValueError("Time data doesnot match format '%Y-%m-%dT%H:%M:%S'")
    return date


def strict_list(arg):
    if not isinstance(arg, list):
        raise ValueError("Argument must be of type list")
    return arg


def clean_null_terms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = clean_null_terms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


class FieldMissing(Exception):
    def __str__(self):
        return "Missing required field"


class RecordNotFound(Exception):
    def __str__(self):
        return "Record Not Found"


class MovieAlreadyExists(Exception):
    def __str__(self):
        return "Movie Already Exists"


class GenreDoesNotExists(Exception):
    def __str__(self):
        return "User does not exists"
