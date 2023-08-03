from flask import render_template, redirect, url_for, flash, Response, request
from flask_login import current_user, login_required
from app import db
from app.models import Meme, User
from . import endpoint
from app.forms import UploadMemeForm
from werkzeug.utils import secure_filename


@endpoint.route("/meme/<int:meme_id>", methods=["GET"])
@login_required
def get_meme(meme_id):
    meme = Meme.query.get_or_404(meme_id)
    return render_template("view_meme.html", meme=meme)


@endpoint.route("/meme/<int:page>", methods=["GET"])
@login_required
def get_memes(page):
    memes = Meme.query.paginate(page=page, per_page=10)
    return render_template("meme.html", memes=memes)


@endpoint.route("/meme/upload", methods=["POST"])
@login_required
def upload_meme():
    form: UploadMemeForm = UploadMemeForm()
    if form.validate_on_submit():
        upload = form.file.data
        url = form.url.data
        private = form.private.data
        if upload:
            meme = Meme.from_upload(upload, current_user.id, private)
            db.session.add(meme)
            db.session.commit()
        elif url:
            meme = Meme.from_url(url, current_user.id, private)
            meme.__setattr__("url", url)
            db.session.add(meme)
            db.session.commit()
    return redirect(url_for("routes.index_page"))
