import importlib
import os

import falcon
from mongoengine import connect

from src.middleware.cors_middleware import CORSMiddleware
from src.api.videos_api import VideosAPI
from src.api.health_api import PingAPI


settings = importlib.import_module("src.settings.{}".format(os.getenv("ENV", "dev")))

VERSION = "v1"


def initialize() -> falcon.API:
    """iInitialize the falcon api and our router
    :return: an initialized falcon.API
    """

    # Create our WSGI application
    # media_type set for json:api compliance
    api = falcon.API(middleware=[CORSMiddleware()])

    # Routes
    api.add_route(f"/{VERSION}/videos", VideosAPI())
    api.add_route(f"/{VERSION}/ping", PingAPI())
    return api


def run() -> falcon.API:
    """
    :return: an initialized falcon.API
    """
    connect(
        settings.MONGODB_DATABASE,
        host=settings.MONGODB_HOST,
        port=int(settings.MONGODB_PORT),
        username=settings.MONGODB_USER,
        password=settings.MONGODB_PASS,
    )
    return initialize()
