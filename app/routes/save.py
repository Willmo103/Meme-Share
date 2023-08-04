from flask import jsonify, request
from . import endpoint
from flask_login import current_user, login_required
from app.models import Meme, User
from app import db


@endpoint.route("/toggle_save_meme", methods=["POST"])
@login_required
def toggle_save_meme():
    meme_id = request.form.get("meme_id")
    meme = Meme.query.get(meme_id)
    user_id = current_user.id

    meme = Meme.query.get(meme_id)

    if meme.saved_by_user(user_id):
        User.query.get(user_id).unsave_meme(meme)
        db.session.commit()
    else:
        User.query.get(user_id).save_meme(meme)
        db.session.commit()

    return jsonify(status="success")


@endpoint.route("/toggle_like_meme", methods=["POST"])
@login_required
def toggle_like_meme():
    meme_id = request.form.get("meme_id")
    meme = Meme.query.get(meme_id)
    user_id = current_user.id

    if meme.liked_by_user(user_id):
        User.query.get(user_id).unlike_meme(meme)
        db.session.commit()
    else:
        User.query.get(user_id).like_meme(meme)
        db.session.commit()

    return jsonify(status="success")
