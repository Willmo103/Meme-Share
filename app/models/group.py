# filename: group.py
# filepath: app\models\group.py

from app import db
from sqlalchemy.orm import Mapped


class Group(db.Model):
    """
    Create a Group model.

    @field id: The id of the group.
    @field name: The name of the group.
    @field memes: The memes in the group.
    @field owner: The owner of the group.
    @field private: Whether the group is private.
    @field members: The members of the group.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    memes: Mapped[list] = db.relationship("Meme", backref="group", lazy=True)
    owner: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    private: bool = db.Column(db.Boolean, nullable=False, default=False)
    members: Mapped[list] = db.relationship(
        "User",
        secondary="group_members",
        lazy="subquery",
        backref=db.backref("groups", lazy=True),
    )

    def __init__(self, name: str, owner: int, private: bool) -> None:
        """
        Instantiate an object of the class.
        @param name: The name of the group.
        @param owner: The owner of the group.
        @param private: Whether the group is private.
        @return: None
        """
        self.name = name
        self.owner = owner
        self.private = private

    def __repr__(self) -> str:
        """
        Return a string representation of the object.
        @return: A string representation of the object.
        """
        return f"Group('{self.id}', '{self.name}')"

    def is_private(self) -> bool:
        """
        Check if the group is private.
        @return: Whether the group is private.
        """
        return self.private

    def set_private(self, private: bool) -> None:
        """
        Set the group as private.
        @param private: Whether the group is private.
        @return: None
        """
        self.private = private
        db.session.commit()

    def set_name(self, name: str) -> None:
        """
        Set the name of the group.
        @param name: The name of the group.
        @return: None
        """
        self.name = name
        db.session.commit()

    def add_member(self, user: int) -> None:
        """
        Add a member to the group.
        @param user: The user to add to the group.
        @return: None
        """
        self.members.append(user)
        db.session.commit()

    def remove_member(self, user: int) -> None:
        """
        Remove a member from the group.
        @param user: The user to remove from the group.
        @return: None
        """
        self.members.remove(user)
        db.session.commit()

    def is_member(self, user: int) -> bool:
        """
        Check if a user is a member of the group.
        @param user: The user to check.
        @return: Whether the user is a member of the group.
        """
        return user in self.members

    def is_owner(self, user: int) -> bool:
        """
        Check if a user is the owner of the group.
        @param user: The user to check.
        @return: Whether the user is the owner of the group.
        """
        return user == self.owner

    def get_owner(self) -> int:
        """
        Get the owner of the group.
        @return: The owner of the group.
        """
        return self.owner

    def get_members(self) -> list:
        """
        Get the members of the group.
        @return: The members of the group.
        """
        return self.members

    def get_memes(self) -> list:
        """
        Get the memes of the group.
        @return: The memes of the group.
        """
        return self.memes

    def get_name(self) -> str:
        """
        Get the name of the group.
        @return: The name of the group."""
        return self.name

    def get_id(self) -> int:
        """
        Get the id of the group.
        @return: The id of the group.
        """
        return self.id

    def get_private(self) -> bool:
        """
        Get the privacy of the group.
        @return: The privacy of the group."""
        return self.private
