# filename: meme.py
# filepath: app\models\meme.py

from PIL import Image
from app import db
from datetime import datetime
from sqlalchemy.orm import Mapped
import os, requests, uuid
from urllib.parse import urlparse
from io import BytesIO

_upload_folder = os.environ.get("UPLOAD_FOLDER")
_thumb_folder = os.path.abspath(os.path.join(_upload_folder, "thumbnails"))


class Meme(db.Model):
    """
    Create a Meme model.

    This model should have the following attributes:
    - id (int, primary key)
    - date_posted (datetime, not nullable, default=datetime.utcnow)
    - posted_by (int, foreign key to user.id)
    - url (str, nullable)
    - filename (str, nullable)
    - filepath (str, nullable)
    - thumbnail (str, nullable)
    - thumbnail_path (str, nullable)
    - deleted (bool, not nullable, default=False)
    - private (bool, not nullable, default=False)

    This model should have the following methods:
    - __init__ (instantiate an object of the class)
    - __repr__ (return a string representation of the object)
    - create_thumbnail (create a thumbnail of the meme)
    - from_url (create a meme from a URL)
    - from_upload (create a meme from an uploaded file)
    - check_seen_by_user (check if a user has seen the meme)
    - seen_by_user (add a user to the list of users who have seen the meme)
    - get_comments (return the comments on the meme)
    - save (save the meme to the database)
    - delete (delete the meme from the database)
    - get_id (get the id of the meme)
    - get_date_posted (get the date posted of the meme)
    - get_posted_by (get the user who posted the meme)
    - get_url (get the URL of the meme)
    - get_filename (get the filename of the meme)
    - get_filepath (get the filepath of the meme)
    - get_thumbnail (get the thumbnail of the meme)
    - get_thumbnail_path (get the thumbnail path of the meme)
    - get_deleted (get whether the meme is deleted)
    - get_private (get whether the meme is private)
    - get_group_id (get the id of the group the meme is in)
    - get_seen_by (get the users who have seen the meme)
    - get_comments (get the comments on the meme)
    - update (update the meme in the database)
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
    url: str = db.Column(db.String(100), nullable=True, default=None)
    filename: str = db.Column(db.String(100), nullable=True, default=None)
    filepath: str = db.Column(db.String(100), nullable=True, default=None)
    sm_thumbnail_path = db.Column(db.String(100), nullable=True, default=None)
    md_thumbnail_path = db.Column(db.String(100), nullable=True, default=None)
    lg_thumbnail_path = db.Column(db.String(100), nullable=True, default=None)
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
        self.create_thumbnail('sm')
        self.create_thumbnail('md')
        self.create_thumbnail('lg')

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Meme('{self.id}', '{self.filename}')"

    def create_thumbnail(self, size_type='md') -> bool:
        """Create thumbnails of the meme with different sizes."""
        # Sizes mapping
        size_mapping = {'sm': (150, 150), 'md': (350, 350), 'lg': (700, 700)}
        size = size_mapping.get(size_type, (350, 350))
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
        return self.sm_thumbnail_path

    def get_md_thumbnail(self) -> str:
        return self.md_thumbnail_path

    def get_lg_thumbnail(self) -> str:
        return self.lg_thumbnail_path

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

    @classmethod
    def from_url(cls, url, posted_by, private, thumbnail_sizes=[(350, 350)]):
        """Create a meme from a URL."""
        # Download the image from the URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download image from {url}")
            return None

        # Open the image with PIL to remove EXIF data
        img = Image.open(BytesIO(response.content))

        # Generate a unique filename
        unique_filename = str(uuid.uuid4()) + '.png'

        # Create the full file path
        filepath = os.path.join(_upload_folder, unique_filename)

        # Save the original image
        img.save(filepath)


        # Create a Meme object with the downloaded image and thumbnails
        meme = cls(posted_by, unique_filename, private)

        return meme

    @classmethod
    def from_upload(cls, file, posted_by, private):
        """Create a meme from an uploaded file."""
        # Generate a unique filename
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]

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
