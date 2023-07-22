from flask import render_template, redirect, url_for, flash, Response, request
from flask_login import current_user, login_required
from app import db
from app.models import Meme, User
from . import endpoint


@endpoint.route("/meme/<page:int>", methods=["GET"])
@login_required
def get_memes(page):
    memes = Meme.query.paginate(page=page, per_page=10)
    return render_template("meme.html", memes=memes)


@endpoint.route("/meme/upload", methods=["GET"])
@login_required
def upload_meme():
    # form = UploadMemeForm()
    ...
