from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config

import os
# Created without an app sp that models and routes can import them at module
# level. They get bound to a specific app inside create_app().
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Build and return a configured Flask application.
    Taking the config class as an argument lets test build an app pointed at
    a throwaway database without changing any application code.
    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True,
        origins=os.environ.get("FRONTEND_URL", "http://localhost:5173").split(","))

    # from_object copies every uppercase attribute off the class into app.config
    app.config.from_object(config_class)

    # Second phase of initialization: attach the extensions to this app
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models   # ensures the models are registered with SQLAlchemy

    # Imported here rather than at the top because each routes module imports
    # db from this file, which would be a circular import
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.skills import skills_bp
    app.register_blueprint(skills_bp)

    from app.routes.postings import postings_bp
    app.register_blueprint(postings_bp)

    return app