# Import all models from app\models\__init__.py
from app import db

group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

saved_memes = db.Table('saved_memes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('meme_id', db.Integer, db.ForeignKey('meme.id'), primary_key=True)
)

from .user import User as User
from .meme import Meme as Meme
