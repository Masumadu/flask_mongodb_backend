from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from healthcheck import HealthCheck

me = MongoEngine()
ma = Marshmallow()
cors = CORS()
healthcheck = HealthCheck()
