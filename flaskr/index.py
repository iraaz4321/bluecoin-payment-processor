from flask import (
    Blueprint, redirect, render_template, session, current_app, request
)
from flaskr.db import get_db

bp = Blueprint('index', __name__, url_prefix="/")

@bp.route("/payment/", methods=('GET',))
def index():

    wallet = request.args.get("a")
    print(wallet)
    with get_db() as db:
        cursor = db.execute("SELECT * FROM pending WHERE wallet=?", (wallet,))
        pending_records = cursor.fetchone()
    if pending_records is None:
        return "Expired transaction."
    wallet, amount, _, _, _= list(pending_records)

    transaction = {"cost": amount, "account": wallet}
    print("DATA", flush=True)
    return render_template("index.html", transaction=transaction)

@bp.route("/terms/", methods=('GET',))
def terms():
    return render_template("terms.html")