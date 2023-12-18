from flaskr.db import get_db
from flaskr.utils.api_utils import create_account, delete_account, balance, transfer
import secrets
import string
import os

def get_password_by_username(username):
    db = get_db()
    cursor = db.execute(
        "SELECT password FROM wallets WHERE username = ?",
        (username,),
    )
    result = cursor.fetchone()

    if result:
        return result[0]  # Assuming there is only one password for a given username
    else:
        return None  # Username not found

def random_generate(length=64):
    possible = "".join((string.ascii_letters, string.digits))
    passw = "".join(secrets.choice(possible) for i in range(length))
    return passw


def generate_wallet():
    name = random_generate(16)
    password = random_generate(64)
    create_account(name, password)

    db = get_db()
    db.execute(
        "INSERT INTO wallets (username, password) VALUES (?, ?)",
        (name, password),
    )
    db.commit()
    return name

def get_balance(wallet):
    return balance(wallet, get_password_by_username(wallet))
