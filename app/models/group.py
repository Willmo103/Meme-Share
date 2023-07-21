from app import db
from sqlalchemy.orm import Mapped
from .tables import group_members

class Group(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    memes: Mapped[list] = db.relationship("Meme", backref="group", lazy=True)
    owner: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    private: bool = db.Column(db.Boolean, nullable=False, default=False)
    members: Mapped[list] = db.relationship("User", secondary="group_members", lazy="subquery", backref=db.backref("groups", lazy=True))

def __init__(self, name: str, owner: int, private: bool) -> None:
        self.name = name
        self.owner = owner
        self.private = private

def __repr__(self) -> str:
    return f"Group('{self.id}', '{self.name}')"

def save(self) -> None:
    db.session.add(self)
    db.session.commit()

def delete(self) -> None:
    db.session.delete(self)
    db.session.commit()

def is_private(self) -> bool:
    return self.private

def set_private(self, private: bool) -> None:
    self.private = private
    db.session.commit()

def set_name(self, name: str) -> None:
    self.name = name
    db.session.commit()

def add_member(self, user: int) -> None:
    self.members.append(user)
    db.session.commit()

def remove_member(self, user: int) -> None:
    self.members.remove(user)
    db.session.commit()

def is_member(self, user: int) -> bool:
    return user in self.members

def is_owner(self, user: int) -> bool:
    return user == self.owner

def get_owner(self) -> int:
    return self.owner

def get_members(self) -> list:
    return self.members

def get_memes(self) -> list:
    return self.memes

def get_name(self) -> str:
    return self.name

def get_id(self) -> int:
    return self.id

def get_description(self) -> str:
    return self.description

def get_private(self) -> bool:
    return self.private
