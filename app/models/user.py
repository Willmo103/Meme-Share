from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager, db
from sqlalchemy.orm import Mapped
from .tables import saved_memes
import os


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


# create the user model
class User(db.Model, UserMixin):
    """
    Create a User model.

    This model should have the following attributes:
    - id (int, primary key)
    - username (str, unique, not nullable)
    - email (str, unique, not nullable)
    - password (str, not nullable)
    - memes (list, backref="posted_memes", lazy=True)
    - saved_memes (list, secondary="saved_memes", lazy="subquery", backref=db.backref("saved_by", lazy=True))
    - is_admin (bool, not nullable, default=False)

    This model should have the following methods:
    - __init__ (instantiate an object of the class)
    - __repr__ (return a string representation of the object)
    - set_password (set the password of the user)
    - check_password (check if the password is correct)
    - forgot_password (set a temporary password for the user)
    - save (save the user to the database)
    - delete (delete the user from the database)
    - is_admin (check if the user is an admin)
    - set_admin (set the user as an admin)
    - admin_login (check if the user is an admin and the password is correct)
    - _set_temp_password (set a temporary password for the user)
    """

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(20), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password: str = db.Column(db.String(60), nullable=False)
    memes: Mapped[list] = db.relationship("Meme", backref="posted_memes", lazy=True)
    saved_memes: Mapped[list] = db.relationship(
        "Meme",
        secondary="saved_memes",
        lazy="subquery",
        backref=db.backref("saved_by", lazy=True),
    )
    is_admin: bool = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username: str, email: str, password: str) -> None:
        """
        Instantiate an object of the class.

        @param username: The username of the user.
        @param email: The email of the user.
        @param password: The password of the user.
        @return: None
        """
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"User('{self.id}', '{self.username}')"

    def set_password(self, password: str) -> None:
        """Set the password of the user.
        @param password: The password of the user.
        @return: None
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the password is correct.
        @param password: The password of the user.
        @return: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password, password)

    def forgot_password(self, new_password: str, temp: str) -> None:
        """
        Set a temporary password for the user.
        @param new_password: The new password of the user.
        @param temp: The temporary password of the user.
        @return: None
        """
        if temp == self.password:
            self.set_password(new_password)
            db.session.commit()

    def _set_temp_password(self) -> None:
        """
        Set a temporary password for the user.
        @return: None
        """
        import random
        import string

        temp = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        self.set_password(temp)
        # send the temp password to the user's email
        db.session.commit()

    def save(self) -> None:
        """
        Save the user to the database.
        @return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the user from the database.
        @return: None
        """
        db.session.delete(self)
        db.session.commit()

    def is_admin(self) -> bool:
        """
        Check if the user is an admin.
        @return: True if the user is an admin, False otherwise.
        """
        return self.is_admin

    def set_admin(self, is_admin: bool) -> None:
        """
        Set the user as an admin.
        @param is_admin: Whether the user is an admin.
        @return: None
        """
        self.is_admin = is_admin
        db.session.commit()

    def admin_login(self, password: str) -> bool:
        """
        Check if the user is an admin and the password is correct.
        @param password: The password of the user.
        @return: True if the user is an admin and the password is correct, False otherwise.
        """
        return (
            check_password_hash(os.getenv("ADMIN_PASSWORD"), password) and self.is_admin
        )
