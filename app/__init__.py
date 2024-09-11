# initialize the app

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.config import Config

app = Flask(__name__)
csrf = CSRFProtect(app)

# Load the config file
app.config.from_object(Config)

# Initialize CSRF protection
csrf.init_app(app)

from app import routes