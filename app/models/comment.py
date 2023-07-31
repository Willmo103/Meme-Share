from datetime import datetime
from app import db


class Comment(db.Model):
    """
    Create a Comment model.

    This model should have the following attributes:
    - id (int, primary key)
    - date_posted (datetime, not nullable, default=datetime.utcnow)
    - posted_by (int, foreign key to user.id)
    - meme_id (int, foreign key to meme.id)
    - content (str, not nullable)

    This model should have the following methods:
    - __init__ (instantiate an object of the class)
    - __repr__ (return a string representation of the object)
    - save (save the comment to the database)
    - delete (delete the comment from the database)
    - get_id (get the id of the comment)
    - get_date_posted (get the date posted of the comment)
    - get_posted_by (get the user who posted the comment)
    - get_meme_id (get the id of the meme the comment is on)
    - get_content (get the content of the comment)
    - update (update the comment in the database)
    """

    id: int = db.Column(db.Integer, primary_key=True)
    date_posted: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    posted_by: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    meme_id: int = db.Column(db.Integer, db.ForeignKey("meme.id"), nullable=False)
    content: str = db.Column(db.String(1000), nullable=False)

    def __init__(
        self, posted_by: int, meme_id: int, content: str, date_posted: datetime = None
    ) -> None:
        """
        Instantiate an object of the class.
        @param posted_by: The user who posted the comment.
        @param meme_id: The meme the comment is on.
        @param content: The content of the comment.
        @param date_posted: The date the comment was posted.
        @return: None
        """
        self.posted_by = posted_by
        self.meme_id = meme_id
        self.content = content
        if date_posted is not None:
            self.date_posted = date_posted

    def __repr__(self) -> str:
        """
        Return a string representation of the object.
        @return: A string representation of the object.
        """
        return f"<Comment {self.id}>"

    def save(self):
        """
        Save the comment to the database.
        @return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the comment from the database.
        @return: None
        """
        db.session.delete(self)
        db.session.commit()

    def update(self, content: str):
        """
        Update the comment in the database.
        @param content: The new content of the comment.
        @return: None
        """
        self.content = content
        db.session.commit()

    def get_id(self) -> int:
        """
        Get the id of the comment.
        @return: The id of the comment.
        """
        return self.id

    def get_date_posted(self) -> datetime:
        """
        Get the date posted of the comment.
        @return: The date posted of the comment.
        """
        return self.date_posted

    def get_posted_by(self) -> int:
        """
        Get the user who posted the comment.
        @return: The user who posted the comment.
        """
        return self.posted_by

    def get_meme_id(self) -> int:
        """
        Get the id of the meme the comment is on.
        @return: The id of the meme the comment is on.
        """
        return self.meme_id

    def get_content(self) -> str:
        """
        Get the content of the comment.
        @return: The content of the comment.
        """
        return self.content
