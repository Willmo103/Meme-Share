from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import dotenv, os, logging
from logging.handlers import RotatingFileHandler

# set the project root directory as an environment variable to be used in other modules
os.environ["PROJECT_ROOT"] = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
)
os.environ["ENV_PATH"] = os.path.join(os.environ.get("PROJECT_ROOT"), ".env")
check_for_dotenv = os.path.exists(os.environ.get("ENV_PATH"))

if check_for_dotenv:
    # if the .env file exists, load it into the environment
    dotenv.load_dotenv(dotenv_path=os.environ.get("ENV_PATH"))
    print("loaded environment variables from .env file")
    os.environ["ENV_MODE"] = "dev"
else:
    print("Loading environment variables from system.")
try:
    assert os.environ.get("SQLALCHEMY_DATABASE_URI") is not None
    assert os.environ.get("UPLOAD_FOLDER") is not None
    assert os.environ.get("SECRET_KEY") is not None
    assert os.environ.get("ADMIN_PASSWORD") is not None
except AssertionError as e:
    print("One or more missing environment variables.")
    raise e

# initialize the app configuration with the utils module and Config class
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    UPLOADS_FOLDER = os.environ.get("UPLOAD_FOLDER")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False
    )
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO") or False
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


# create an instance of the Config class
conf = Config()

# initialize the database
db: SQLAlchemy = SQLAlchemy()

# initialize the login manager
login_manager = LoginManager()

# set the login view for the login manager
login_manager.login_view = "routes.login"


# create the app factory function and register the blueprints and database
def create_app():
    # create the flask app instance
    app = Flask(__name__)

    # load the app configuration
    app.config.from_object(Config)

    log_level = logging.INFO

    # Define the log file path
    log_file_path = f"{os.environ['PROJECT_ROOT']}/app.log"

    # Create a log formatter
    log_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create a rotating file handler to log messages to the file
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
    file_handler.setFormatter(log_formatter)

    # Get the app's logger and add the file handler to it
    app.logger.addHandler(file_handler)

    # Set the log level for the app's logger
    app.logger.setLevel(log_level)

    # initialize the database
    db.init_app(app)

    # initialize the login manager
    login_manager.init_app(app)

    # using the app context, register the blueprints and models
    with app.app_context():

        # import the routes and models modules
        from . import routes
        from . import models

        # register the blueprints
        app.register_blueprint(routes.endpoint)

        # create the database tables if they do not exist
        db.create_all()

        # return the app instance
        return app


# create the app instance
app = create_app()
