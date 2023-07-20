from app import db

class Save(db.Model):
    user: int = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    meme: int = db.Column(db.Integer, db.ForeignKey("meme.id"), primary_key=True)
