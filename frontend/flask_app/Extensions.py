from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate

DATABASE = SQLAlchemy()
CACHE= Cache()
LOGIN_MANAGER= LoginManager()
# Initialize Authlib OAuth client for Auth0
oauth = OAuth()