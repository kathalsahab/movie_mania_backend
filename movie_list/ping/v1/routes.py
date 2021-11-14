"""Routes related to Ping feature.
This is a sample file, will bere moved later.
"""
# system & installed imports
import logging
from flask_restx import Resource, Namespace, fields

# application level import
from . import controllers as c

# Swagger UI categorising of end points under namespaces
api = Namespace("Ping", description="Tests weather the server returns a responses")

ping_post_request_model = api.model(
    "Ping POST request",
    {"name": fields.String(description="name of ping", required=True)},
)


@api.route("/ping", endpoint="ping_v1")
class Ping(Resource):
    def get(self):
        """Returns PONG"""
        logging.debug("GET LIST OF PING")
        return c.handle_ping()
