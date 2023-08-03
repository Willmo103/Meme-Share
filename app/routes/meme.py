from flask import render_template, redirect, url_for, flash, Response, request
from flask_login import current_user, login_required
from app import db
from app.models import Meme, User
from . import endpoint
from app.forms import UploadMemeForm

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


@endpoint.route("/meme/upload", methods=["GET"])
@login_required
def upload_meme():
    form = UploadMemeForm()
    if form.validate_on_submit():
        file = form.image.data
        private = form.private.data
        meme = Meme.from_upload(file, current_user.id, private)
        if meme:
            db.session.add(meme)
            db.session.commit()
            flash('Meme uploaded successfully!', 'success')
            return redirect(url_for('endpoint.get_meme', meme_id=meme.id))
        else:
            flash('An error occurred while uploading the meme. Please try again.', 'error')
    return render_template("upload_meme.html", form=form)
