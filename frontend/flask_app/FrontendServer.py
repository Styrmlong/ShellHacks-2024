# FrontendServer.py

from flask_migrate import Migrate
# Removed: from jupyter_core.migrate import migrate  # This was incorrect

import frontend.flask_app.Config as Config
from flask import Flask, render_template, redirect, url_for
from Extensions import oauth, DATABASE  # Ensure Extensions.py initializes SQLAlchemy as DATABASE
from Config import config, SQLALCHEMY_DATABASE_URI  # Load configuration
from Blueprints.User import user_bp  # Import the user authentication blueprint
from Blueprints.Assesment import assesment_bp
from Blueprints.Testing import test_bp

app = Flask(__name__)
app.secret_key = config["WEBAPP"]["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Initialize extensions with Flask app
DATABASE.init_app(app)
migrate = Migrate(app, DATABASE)
oauth.init_app(app)

# Auth0 Configuration
auth0_config = config['AUTH0']
domain = auth0_config["DOMAIN"]
client_id = auth0_config["CLIENT_ID"]
client_secret = auth0_config["CLIENT_SECRET"]

# Register the Auth0 OAuth client
oauth.register(
    'auth0',
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f'https://{domain}/.well-known/openid-configuration'
)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(assesment_bp)
app.register_blueprint(test_bp)

# Home route
@app.route('/')
def home():
    return redirect(url_for('user.profile'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
