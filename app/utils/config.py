import os, hashlib


def init_db_config():
    env_file = os.environ.get("ENV_PATH")
    try:
        os.environ.get("DATABASE_URL_POSTGRES")
        os.environ["DB_TYPE"] = "postgres"
    except KeyError:
        os.environ["DB_TYPE"] = "postgres"
        try:
            os.environ.get("SQLALCHEMY_DATABASE_URI_SQLITE")
        except KeyError:
            os.environ["SQLALCHEMY_DATABASE_URI_SQLITE"] = "sqlite:///notes.db"
            with open(env_file, "a") as f:
                f.write(f"DATABASE_URL_SQLITE=sqlite:///meme_share.db")
    if os.environ["DB_TYPE"] == "postgres":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_POSTGRES")
    elif os.environ["DB_TYPE"] == "sqlite":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_SQLITE")
    else:
        raise Exception("Database type not supported")
    os.environ["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    with open(env_file, "r") as f:
        lines = f.readlines()
    if not any("SQLALCHEMY_DATABASE_URI" in line for line in lines):
        with open(env_file, "w") as f:
            for line in lines:
                if "SQLALCHEMY_DATABASE_URI" not in line:
                    f.write(line)

        with open(env_file, "a") as f:
            f.write(f"""\nSQLALCHEMY_DATABASE_URI='{SQLALCHEMY_DATABASE_URI}'""")
    return


def init_uploads_folder():
    env_file = os.environ.get("ENV_PATH")
    root = os.environ.get("PROJECT_ROOT")
    try:
        UPLOADS_FOLDER = os.environ.get("UPLOAD_FOLDER")
        if not os.path.isabs(os.environ["UPLOAD_FOLDER"]):
            UPLOADS_FOLDER = os.path.join(root, os.environ["UPLOAD_FOLDER"])
            os.environ["UPLOAD_FOLDER"] = UPLOADS_FOLDER
            with open(env_file, "r") as f:
                lines = f.readlines()
            with open(env_file, "w") as f:
                for line in lines:
                    if not line.startswith("UPLOAD_FOLDER"):
                        f.write(line)
            with open(env_file, "a") as f:
                f.write(f"""\nUPLOAD_FOLDER='{os.environ["UPLOAD_FOLDER"]}\'""")
    except KeyError:
        UPLOADS_FOLDER = os.path.join(root, "uploads")
        os.environ["UPLOAD_FOLDER"] = UPLOADS_FOLDER
        with open(env_file, "a") as f:
            f.write(f"""\nUPLOAD_FOLDER='{os.environ["UPLOAD_FOLDER"]}\'""")
    if not os.path.exists(os.environ["UPLOAD_FOLDER"]):
        os.mkdir(os.environ["UPLOAD_FOLDER"])
    return


def init_secret_key():
    env_file = os.environ.get("ENV_PATH")
    try:
        os.environ.get("SECRET_KEY")
    except KeyError:
        SECRET_KEY = hashlib.sha256(os.urandom(64)).hexdigest()
        os.environ["SECRET_KEY"] = SECRET_KEY
        with open(env_file, "a") as f:
            f.write(f'\nSECRET_KEY={os.environ["SECRET_KEY"]}')
    return
