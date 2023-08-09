import os
from flask import render_template, redirect, url_for, flash, Response, request
from flask_login import current_user, login_required
from app import db
from . import endpoint
from app.models import User, Group, Meme
from app.forms import AdminLoginForm, RegistrationForm


@endpoint.route("/user", methods=["GET"])
@login_required
def user():
    return render_template("user_page.html")


@endpoint.route("/user/image/", defaults={"id": None}, methods=["GET", "POST"])
@endpoint.route("/user/image/<int:id>", methods=["GET", "POST"])
def choose_profile_image(id):
    if request.method == "POST":
        image = request.args.get("file")
        user = User.query.get_or_404(id)
        user.set_profile_image(image)
        if request.endpoint  == "endpoint.choose_profile_image":
            return redirect(url_for("endpoint.login"))
        return redirect(url_for("endpoint.user"))
    if request.method == "GET":
        default_images = [
            image for image in os.listdir("app/static/images/default_images")
        ]
        print(default_images)
        return render_template("set_image.html", default_images=default_images, id=id)


@endpoint.route("/user/<int:id>", methods=["GET"])
@login_required
def user_id(id):
    user = User.query.get_or_404(id)
    return render_template("user.html", user=user)


@endpoint.route("/user/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(id):
    if current_user.id == id:
        user = User.query.get_or_404(id)
        form = RegistrationForm()
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("endpoint.user", id=user.id))
        elif request.method == "GET":
            form.username.data = user.username
            form.email.data = user.email
        return render_template("edit_user.html", form=form)
    else:
        flash("You are not authorized to edit this user.")
        return redirect(url_for("endpoint.index"))


@endpoint.route("/user/<int:id>/delete", methods=["POST"])
@login_required
def delete_user(id):
    form = AdminLoginForm()
    if form.validate_on_submit():
        User.admin_login(form.password.data)
        flash("You have successfully logged in as an admin.")
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted.")
        return redirect(url_for("endpoint.index"))
    elif current_user.id == id:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted.")
        return redirect(url_for("endpoint.logout"))
    else:
        flash("You are not authorized to delete this user.")
    return redirect(url_for("endpoint.index"))
