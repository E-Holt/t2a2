from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

#db = t2a2_coffee_db in postgres, admin = db_dev password = 123456

# Create the objects
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # Create the flask app object
    app = Flask(__name__)

    app.config.from_object("config.app_config")

    # Initialise the instances of the objects
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import the blueprint commands
    from commands import db_commands
    app.register_blueprint(db_commands)

    # Import the registerable controllers
    from controllers import Registerable_controllers
    for controller in Registerable_controllers:
        app.register_blueprint(controller)

    return app