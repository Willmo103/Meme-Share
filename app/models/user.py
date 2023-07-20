from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager, db
import os

@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))

# create the user model
class User(UserMixin, db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(20), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password: str = db.Column(db.String(60), nullable=False)
    memes: list = db.relationship("Meme", backref="posted_memes", lazy=True)
    saved_memes: list = db.relationship("Meme", secondary="saved_memes", lazy="subquery", backref=db.backref("saved_by", lazy=True))
    is_admin: bool = db.Column(db.Boolean, nullable=False, default=False)


    def __init__(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"User('{self.id}', '{self.username}')"

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def forgot_password(self, new_password: str, temp: str) -> None:
        if temp == self.password:
            self.set_password(new_password)
            db.session.commit()

    def _set_temp_password(self) -> None:
        import random
        import string
        temp = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.set_password(temp)
        # send the temp password to the user's email
        db.session.commit()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def is_admin(self) -> bool:
        return self.is_admin

    def set_admin(self, is_admin: bool) -> None:
        self.is_admin = is_admin
        db.session.commit()

    def admin_login(self, password: str) -> bool:
        return check_password_hash(os.getenv("ADMIN_PASSWORD"), password) and self.is_admin
