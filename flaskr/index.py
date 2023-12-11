from flask import (
    Blueprint, redirect, render_template, session, current_app, request
)


bp = Blueprint('index', __name__, url_prefix="/")

@bp.route("/", methods=('GET',))
def index():
    return render_template("index.html")