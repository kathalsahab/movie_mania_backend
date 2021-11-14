"""Environment Specific Config Values should be set here
    """

import os
from urllib.parse import quote_plus as urlquote

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
TRUTHY_VALUES = ["True", True, "true", "1", 1, "yes", "Yes", "Y", "y"]


class BaseConfig(object):
    # Flask variables
    DEBUG = False
    TESTING = False
    BUNDLE_ERRORS = os.getenv("BUNDLE_ERRORS", "False") in TRUTHY_VALUES
    PROTOCOL = "https://"

    # To safely convert datetime objects while sending response back to frontend
    RESTX_JSON = {"default": str}
    # for flask restx abort
    ERROR_INCLUDE_MESSAGE = False

    # sql db specific
    APP_DB_USER = os.getenv("APP_DB_USER")
    APP_DB_SECRET = os.getenv("APP_DB_SECRET")
    APP_DB_HOST = os.getenv("APP_DB_HOST")
    APP_DB_PORT = os.getenv("APP_DB_PORT")
    APP_DB_NAME = os.getenv("APP_DB_NAME")
    APP_DB_USE_SSL = os.getenv("APP_DB_USE_SSL", "False") in TRUTHY_VALUES

    # SQLALCHEMY_DATABASE_URI = (
    #     f"mysql://{APP_DB_USER}:%s@{APP_DB_HOST}:{APP_DB_PORT}/{APP_DB_NAME}"
    #     % urlquote(APP_DB_SECRET)
    # )
    # SQLALCHEMY_DATABASE_URI = f"mysql://{APP_DB_USER}:{APP_DB_SECRET}@{APP_DB_HOST}:{APP_DB_PORT}/{APP_DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{APP_DB_USER}:{APP_DB_SECRET}@{APP_DB_HOST}:{APP_DB_PORT}/{APP_DB_NAME}"

    # to disable logs of sqlalchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("APP_DB_TRACK_MODIFICATIONS", "False") in TRUTHY_VALUES
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

    SQLALCHEMY_ECHO = True  # print logs from sql-alchemy for dev and testing


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "tests/db.sqlite")
    SQLALCHEMY_ECHO = True  # print logs from sql-alchemy for dev and testing


class ProductionConfig(BaseConfig):
    pass
