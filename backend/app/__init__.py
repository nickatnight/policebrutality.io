import importlib
import os

import falcon
import mongoengine as mongo

from app.middleware.cors_middleware import CORSMiddleware
from app.resources.video import VideoResource
from app.resources.health import Ping


settings = importlib.import_module("app.settings.{}".format(os.getenv("ENV", "dev")))

VERSION = "v1"

app = falcon.API(middleware=[CORSMiddleware()])

db = mongo.connect(
    settings.MONGODB_DATABASE,
    host=settings.MONGODB_HOST,
    port=int(settings.MONGODB_PORT),
    username=settings.MONGODB_USER,
    password=settings.MONGODB_PASS,
)

app.add_route(f"/{VERSION}/videos", VideoResource())
app.add_route(f"/{VERSION}/ping", Ping())
