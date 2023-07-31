# Import all models from app\models\__init__.py
# filename: app\models\__init__.py

from .user import User as User
from .meme import Meme as Meme
from .group import Group as Group
from .comment import Comment as Comment
from .tables import (
    group_members as group_members,
    saved_memes as saved_memes,
    seen_memes as seen_memes,
    posted_comments as posted_comments,
)
