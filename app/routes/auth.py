from flask import render_template, redirect, url_for, flash, Response
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.forms import LoginForm, RegistrationForm
from . import endpoint

__all__ = [
    "login",
    "logout",
    "register",
]


@endpoint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("routes.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("routes.index_page"))
    return render_template("login.html", title="Sign In", form=form)


@endpoint.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("routes.index_page"))


@endpoint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        user.save()
        flash(f"New user {form.username.data} has been created!")
        return redirect(url_for("routes.login"))
    return render_template("new_user.html", title="Register", form=form)
