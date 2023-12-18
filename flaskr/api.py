import time

from flask import (
    Blueprint, redirect, render_template, session, current_app, request, jsonify
)
from flaskr.db import get_db
from flaskr.utils import account_utils

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route("/payment/", methods=('POST',))
def create_payment():
    data = request.json
    amount = data.get('amount')
    receiver = data.get('receiver')
    redirect_url = data.get('redirect_url', None)

    if receiver is None:
        return "The 'recipient' parameter is missing or invalid", 400

    if amount is None:
        return "The 'amount' parameter is missing or invalid.", 400

    wallet = account_utils.generate_wallet()
    payment_id = account_utils.random_generate(64)
    db = get_db()
    db.execute(
        "INSERT INTO pending (wallet, amount, receiver, creation_time, redirect_url) VALUES (?, ?, ?, ?, ?)",
        (wallet, amount, receiver, int(time.time()), redirect_url),
    )

    return jsonify({"account": wallet, "payment_url": request.url_root+f"payment/?a={payment_id}"})