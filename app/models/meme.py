# filename: meme.py
# filepath: app\models\meme.py

import pathlib
from PIL import Image
from app import db
from datetime import datetime
from sqlalchemy.orm import Mapped
import os, requests, uuid
from io import BytesIO
from werkzeug.datastructures import FileStorage
from app import conf
from . import User

_upload_folder = conf.UPLOADS_FOLDER
_thumb_folder = conf.THUMBNAILS_FOLDER
_static_folder = os.path.join(os.environ.get("PROJECT_ROOT"), "app", "static")


class Meme(db.Model):
    """
    @field id: The id of the meme.
    @field date_posted: The date the meme was posted.
    @field posted_by: The user who posted the meme.
    @field url: The URL of the meme.
    @field filename: The filename of the meme.
    @field filepath: The filepath of the meme.
    @field sm_thumbnail_path: The filepath of the small thumbnail of the meme.
    @field md_thumbnail_path: The filepath of the medium thumbnail of the meme.
    @field lg_thumbnail_path: The filepath of the large thumbnail of the meme.
    @field deleted: Whether the meme is deleted.
    @field private: Whether the meme is private.
    @field group_id: The id of the group the meme is in.
    @field seen_by: The users who have seen the meme.
    @field comments: The comments on the meme.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    date_posted: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    posted_by: int = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True,
        default=None,
    )
    url: str = db.Column(db.String(200), nullable=True, default=None)
    filename: str = db.Column(db.String(200), nullable=True, default=None)
    filepath: str = db.Column(db.String(200), nullable=True, default=None)
    sm_thumbnail_path = db.Column(db.String(200), nullable=True, default=None)
    md_thumbnail_path = db.Column(db.String(200), nullable=True, default=None)
    deleted: bool = db.Column(db.Boolean, nullable=False, default=False)
    private: bool = db.Column(db.Boolean, nullable=False, default=False)
    group_id: int = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=True)
    seen_by: Mapped[list] = db.relationship(
        "User",
        secondary="seen_memes",
        lazy="subquery",
        backref=db.backref("seen_memes", lazy=True),
    )
    comments: Mapped[list] = db.relationship(
        "Comment", backref="meme", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, posted_by: int, filename: str, private: bool) -> None:
        """
        Instantiate an object of the class.

        @param posted_by: The user who posted the meme.
        @param filename: The filename of the meme.
        @param private: Whether the meme is private.

        @return: None

        """
        self.posted_by = posted_by
        self.filename = filename
        self.filepath = os.path.join(_upload_folder, filename)
        self.private = private
        self.create_thumbnail("sm")
        self.create_thumbnail("md")

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Meme('{self.id}', '{self.filename}')"

    def create_thumbnail(self, size_type="md") -> bool:
        """Create thumbnails of the meme with different sizes."""
        # Sizes mapping
        size_mapping = {"sm": (309, 309), "md": (468, 468)}
        size = size_mapping.get(size_type)
        try:
            img = Image.open(self.filepath)
            img.thumbnail(size)
            thumb_filename = f"{size_type}_thumbnail_{self.filename}"
            thumb_path = os.path.join(_thumb_folder, thumb_filename)
            img.save(thumb_path)
            setattr(self, f"{size_type}_thumbnail_path", thumb_path)
            return True
        except Exception as err:
            print(err)
            return False

    def get_sm_thumbnail(self) -> str:
        rel_path = os.path.relpath(self.sm_thumbnail_path, _static_folder)
        return self.sm_thumbnail_path

    def render_sm_thumb(self):
        return f"uploads/thumbnails/sm_thumbnail_{self.filename}"

    def render_md_thumb(self):
        return f"uploads/thumbnails/md_thumbnail_{self.filename}"

    def render_lg_thumb(self):
        return f"uploads/thumbnails/lg_thumbnail_{self.filename}"

    def render_full(self):
        return self.filename

    def get_md_thumbnail(self) -> str:
        rel_path = os.path.relpath(self.md_thumbnail_path, _static_folder)
        return rel_path

    def get_lg_thumbnail(self) -> str:
        rel_path = os.path.relpath(self.lg_thumbnail_path, _static_folder)
        return rel_path

    def check_seen_by_user(self, user_id: int) -> bool:
        """Check if a user has seen the meme."""
        return user_id in [user.id for user in self.seen_by]

    def seen_by_user(self, user_id: int) -> None:
        """Add a user to the list of users who have seen the meme."""
        if not self.check_seen_by_user(user_id):
            self.seen_by.append(user_id)
            self.save()

    def get_comments(self):
        """Return the comments on the meme."""
        return self.comments

    def save(self) -> None:
        """Save the meme to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        """Delete the meme from the database."""
        db.session.delete(self)
        db.session.commit()

    def get_id(self) -> int:
        """Get the id of the meme."""
        return self.id

    def get_date_posted(self) -> datetime:
        """Get the date posted of the meme."""
        return self.date_posted

    def get_posted_by(self) -> int:
        """Get the user who posted the meme."""
        return self.posted_by

    def get_url(self) -> str:
        """Get the URL of the meme."""
        return self.url

    def get_filename(self) -> str:
        """Get the filename of the meme."""
        return self.filename

    def get_filepath(self) -> str:
        """Get the filepath of the meme."""
        return self.filepath

    def get_deleted(self) -> bool:
        """Get whether the meme is deleted."""
        return self.deleted

    def get_private(self) -> bool:
        """Get whether the meme is private."""
        return self.private

    def get_group_id(self) -> int:
        """Get the id of the group the meme is in."""
        return self.group_id

    def get_seen_by(self) -> list:
        """Get the users who have seen the meme."""
        return self.seen_by

    def update(self) -> None:
        """Update the meme in the database."""
        db.session.commit()

    def get_username(self) -> str:
        """Get the username of the user who posted the meme."""
        return User.query.get(self.posted_by).get_username()

    @classmethod
    def from_url(cls, url: str, posted_by: int, private: bool):
        """Create a meme from a URL."""
        # Download the image from the URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download image from {url}")
            return None

        # Open the image with PIL to remove EXIF data
        img = Image.open(BytesIO(response.content))

        # Generate a unique filename
        unique_filename = str(uuid.uuid4()) + ".png"

        # Create the full file path
        filepath = os.path.join(_upload_folder, unique_filename)

        # Save the original image
        img.save(filepath)

        # Create a Meme object with the downloaded image and thumbnails
        meme = cls(posted_by, unique_filename, private)

        return meme

    @classmethod
    def from_upload(cls, file: FileStorage, posted_by: int, private: bool):
        """Create a meme from an uploaded file."""
        # Generate a unique filename
        unique_filename = str(uuid.uuid4()) + "." + file.filename.split(".")[-1]

        # Create the full file path
        filepath = os.path.join(_upload_folder, unique_filename)

        # Save the uploaded file
        file.save(filepath)

        # Open the image with PIL to remove EXIF data
        img = Image.open(filepath)
        img.save(filepath)

        # Create a Meme object with the saved image
        meme = cls(posted_by, unique_filename, private)

        return meme

    def fix_db_urls(self):
        pathlib.Path(self.sm_thumbnail_path).resolve()
        pathlib.Path(self.md_thumbnail_path).resolve()
        pathlib.Path(self.lg_thumbnail_path).resolve()
        pathlib.Path(self.filepath).resolve()

    def saved_by_user(self, user_id: int) -> bool:
        """Check if a user has saved the meme."""
        return user_id in [user.id for user in self.saved_by]

    def liked_by_user(self, user_id: int) -> bool:
        """Check if a user has liked the meme."""
        return user_id in [user.id for user in self.liked_by]

    def delete_files(self):
        """Delete the meme files from the filesystem."""
        os.remove(os.path.abspath(self.filepath))
        os.remove(os.path.abspath(self.sm_thumbnail_path))
        os.remove(os.path.abspath(self.md_thumbnail_path))
        os.remove(os.path.abspath(self.lg_thumbnail_path))
