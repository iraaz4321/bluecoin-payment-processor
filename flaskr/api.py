import time

from flask import (
    Blueprint, redirect, render_template, session, current_app, request, jsonify
)
from flaskr.db import get_db
from flaskr.utils import account_utils, api_utils

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route("/payment/", methods=('POST',))
def create_payment():
    data = request.json
    amount = data.get('amount')
    receiver = data.get('receiver')
    redirect_url = data.get('redirect_url', None)

    if receiver is None:
        return "The 'receiver' parameter is missing or invalid", 400

    if amount is None:
        return "The 'amount' parameter is missing or invalid.", 400

    wallet = account_utils.generate_wallet()
    db = get_db()
    db.execute(
        "INSERT INTO pending (wallet, amount, receiver, creation_time, redirect_url) VALUES (?, ?, ?, ?, ?)",
        (wallet, amount, receiver, int(time.time()), redirect_url),
    )
    db.commit()
    return jsonify({"account": wallet, "payment_url": request.url_root+f"payment/?a={wallet}"})


@bp.route("/payment_state/", methods=('POST',))
def payment_state():
    data = request.json
    wallet = data.get('account')

    if wallet is None:
        return "The 'account' parameter is missing or invalid", 400

    balance = account_utils.get_balance(wallet)
    with get_db() as db:
        cursor = db.execute("SELECT amount, receiver, redirect_url FROM pending WHERE wallet=?", (wallet,))
        if cursor is None:
            return "Transaction expired!", 404

        transaction_data = list(cursor.fetchone())

    if transaction_data[0] <= balance:
        receiver = transaction_data[1]
        redirect_url = transaction_data[2]
        account_utils.new_taxed_transfer(wallet, receiver, transaction_data[0])
        return jsonify({"paid": balance, "cost": transaction_data[0], "redirect_url": redirect_url})

    return jsonify({"paid": balance, "cost": transaction_data[0]})