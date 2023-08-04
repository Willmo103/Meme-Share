from . import endpoint
from flask import redirect, url_for
from app import db
from app.models import Meme


@endpoint.route("/fix/memes", methods=["GET"])
def fix_memes():
    memes = Meme.query.all()
    for meme in memes:
        meme.fix_db_urls()
        db.session.commit()
    return redirect(url_for("routes.index_page"))


@endpoint.route("/dump/memes", methods=["GET"])
def dump_memes():
    memes = Meme.query.all()
    for meme in memes:
        try:
            meme.delete_files()
        except FileNotFoundError or TypeError:
            pass
        db.session.delete(meme)
        db.session.commit()
    return redirect(url_for("routes.index_page"))
