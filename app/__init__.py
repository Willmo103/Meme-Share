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
    assert os.environ.get("SECRET_KEY") is not None
    assert os.environ.get("ADMIN_PASSWORD") is not None
except AssertionError as e:
    print("One or more missing environment variables.")
    raise e

# initialize the app configuration with the utils module and Config class
class Config:
    """
    @field SQLALCHEMY_DATABASE_URI: The URI for the database.
    @field UPLOADS_FOLDER: The folder where uploaded files are stored.
    @field THUMBNAILS_FOLDER: The folder where thumbnails are stored.
    @field SECRET_KEY: The secret key for the app.
    @field SQLALCHEMY_TRACK_MODIFICATIONS: Whether to track modifications to the database.
    @field SQLALCHEMY_ECHO: Whether to echo SQL statements to the console.
    @field ADMIN_PASSWORD: The password for the admin user.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    UPLOADS_FOLDER = os.environ.get("PROJECT_ROOT") + "/app/static/uploads"
    THUMBNAILS_FOLDER = (
        os.environ.get("PROJECT_ROOT") + "/app/static/uploads/thumbnails"
    )
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False
    )
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO") or False
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


# create the folder structure for the uploads and thumbnails, if they do not exist
os.makedirs(Config.THUMBNAILS_FOLDER, exist_ok=True)

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
    """
    Create the app instance and register the blueprints and database.
    @return: The app instance.
    """
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

        # from .scripts import test_memes
        # test_memes.generate_test_memes()
        # return the app instance
        return app


# create the app instance
app = create_app()
