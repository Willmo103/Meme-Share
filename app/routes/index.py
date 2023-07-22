from flask import redirect, url_for, render_template
from flask_login import current_user
from . import endpoint
import os


@endpoint.route("/")
@endpoint.route("/index", methods=["GET"])
def index_page():
    if not current_user.is_authenticated and os.environ.get("ENV_MODE") != "dev":
        return redirect(url_for("routes.login"))
    else:
        user_id = None
    return render_template(
        "index.html",
        user_id=user_id,
        title="Intragram",
    )
