from flask import render_template, redirect, url_for, flash, Response, request
from flask_login import current_user, login_required
from app import db
from . import endpoint
from app.models import User, Group, Meme

@endpoint.route('/user', methods=['GET'])
@login_required
def user():
    return render_template('user.html')

@endpoint.route('/user/<int:id>', methods=['GET'])
@login_required
def user_id(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)
