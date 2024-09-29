# config.py

import os

CACHE_KEY_PREFIX = "app_cache"
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 8 * 60

HOSTNAME = "127.0.0.1"
SQLPORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "users"

# Determine the absolute path to the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Construct the absolute path to the SQLite database
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'Database', DATABASE + '.db')}"

config = {
    "AUTH0": {
        "CLIENT_ID": "oPGLL3AT4jP8WM0INEIyEm2ZwH8eJ9Nu",
        "CLIENT_SECRET": "vaUpfvekYV0AImXSPpff9Jg4_Lw-GnmIf1Dh3CUf1tYDoPeNShF4rbXrhckXiSqL",
        "DOMAIN": "dev-bbhd7vuhibi44nyh.us.auth0.com",
        "AUDIENCE": "https://shellhacks-auth0-example.com"
    },
    "WEBAPP": {
        "SECRET_KEY": "c7014636f412dd9e04f73d8ea1ebe2c934bd711855d11e3319ced396767795b9"
    }
}
