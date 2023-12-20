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

    with get_db() as db:
        cursor = db.execute("SELECT redirect_url FROM transaction_history WHERE wallet=?", (wallet,))
        if cursor is not None:
            one = cursor.fetchone()
            if one is not None:
                return jsonify({"paid": 0, "cost": 0, "redirect_url": list(one)[0]}), 200

    balance = account_utils.get_balance(wallet)
    with get_db() as db:
        cursor = db.execute("SELECT amount, receiver, redirect_url FROM pending WHERE wallet=?", (wallet,))
        if cursor is None:
            return "Transaction expired!", 404

        transaction_data = list(cursor.fetchone())
    print((transaction_data[0]) <= float(balance), balance, transaction_data[0], transaction_data[1], wallet, flush=True)
    if float(transaction_data[0]) <= float(balance):
        receiver = transaction_data[1]
        redirect_url = transaction_data[2]
        account_utils.new_taxed_transfer(wallet, receiver, float(transaction_data[0]))

        db = get_db()
        db.execute(
            "INSERT INTO transaction_history (receiver, payment_time, amount, redirect_url, wallet) VALUES (?, ?, ?, ?, ?)",
            (receiver, int(time.time()), float(transaction_data[0]), redirect_url, wallet),
        )
        db.commit()

        return jsonify({"paid": balance, "cost": float(transaction_data[0]), "redirect_url": redirect_url}), 200

    return jsonify({"paid": balance, "cost": float(transaction_data[0])}), 204
