
"""
Initialize the Flask application for the Credit Risk Assessment Tool.
This module initializes the Flask application by creating an instance of the Flask class and setting up CSRF protection. It also loads the configuration file and sets up CSRF protection for security purposes.
Attributes:
    app (Flask): The Flask application instance.
    csrf (CSRFProtect): The CSRF protection instance.
"""



from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.config import Config

app = Flask(__name__)
csrf = CSRFProtect(app)

# Load the config file
app.config.from_object(Config)

# Initialize CSRF protection for security purposes
csrf.init_app(app)

from app import routes