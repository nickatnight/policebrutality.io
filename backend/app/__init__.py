import os

import falcon
import mongoengine as mongo

# from app.settings import middleware
from app.resources.video import VideoResource


VERSION = "v1"

app = falcon.API()

db = mongo.connect(
    os.getenv("MONGODB_DATABASE", ""),
    host=os.getenv("MONGODB_HOST", ""),
    port=int(os.getenv("MONGODB_PORT", 27017)),
    username=os.getenv("MONGODB_USER", ""),
    password=os.getenv("MONGODB_PASS", ""),
)

app.add_route(f"/{VERSION}/videos", VideoResource())
