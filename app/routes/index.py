from flask import redirect, url_for, render_template
from flask_login import current_user
from . import endpoint
from app.models import Meme
import os


@endpoint.route("/")
@endpoint.route("/index", methods=["GET"])
def index_page():
    if not current_user.is_authenticated:
        return redirect(url_for("routes.login"))
    user_id = current_user.id
    memes = Meme.query.filter_by(deleted=False).all()
    return render_template(
        "index.html", user_id=user_id, title="Intragram", memes=memes
    )
