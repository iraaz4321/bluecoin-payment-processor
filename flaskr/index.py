from flask import (
    Blueprint, redirect, render_template, session, current_app, request
)


bp = Blueprint('index', __name__, url_prefix="/")

@bp.route("/payment/", methods=('GET',))
def index():
    transaction = {"cost": 50, "account": "placeholder"}
    return render_template("index.html", transaction=transaction)

@bp.route("/terms/", methods=('GET',))
def terms():
    return render_template("terms.html")