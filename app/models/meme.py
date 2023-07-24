# filename: app\models\meme.py
# Model for the Meme class

from PIL import Image
from app import db
from datetime import datetime
from sqlalchemy import or_
import os

_upload_folder = os.environ.get("UPLOAD_FOLDER")


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
    thumbnail: str = db.Column(db.String(100), nullable=True, default=None)
    thumbnail_path: str = db.Column(db.String(100), nullable=True, default=None)
    deleted: bool = db.Column(db.Boolean, nullable=False, default=False)
    private: bool = db.Column(db.Boolean, nullable=False, default=False)
    group_id: int = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

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
        self.thumbnail = f"thumbnail_{filename}"
        self.thumbnail_path = os.path.join(_upload_folder, "thumbnails", self.thumbnail)
        self.private = private
        self.create_thumbnail()

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Meme('{self.id}', '{self.filename}')"

    def create_thumbnail(self, size=(350, 350)) -> bool:
        """Create a thumbnail of the meme."""
        try:
            img = Image.open(self.filepath)
            img.thumbnail(size)
            img.save(self.thumbnail_path)
            return True
        except Exception as err:
            print(err)
            return False

    @classmethod
    def from_url(cls, url, posted_by, private):
        """Create a meme from a URL."""
        # This method should download the image from the URL, save it to the
        # upload folder, and then create a Meme object with the filename of
        # the saved image.
        # ...code to download image...
        filename = ...  # the filename of the downloaded image
        return cls(posted_by, filename, private)

    @classmethod
    def from_upload(cls, file, posted_by, private):
        """Create a meme from an uploaded file."""
        # This method should save the uploaded file to the upload folder,
        # and then create a Meme object with the filename of the saved file.
        # ...code to save uploaded file...
        filename = ...  # the filename of the saved file
        return cls(posted_by, filename, private)
