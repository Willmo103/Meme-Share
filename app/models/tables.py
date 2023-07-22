from app import db

# The following tables are reference tables for the many-to-many relationships
group_members = db.Table(
    "group_members",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True),
)

saved_memes = db.Table(
    "saved_memes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("meme_id", db.Integer, db.ForeignKey("meme.id"), primary_key=True),
)
