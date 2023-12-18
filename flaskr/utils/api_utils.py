import requests


bluecoin_server = "https://darkbluestealth.pythonanywhere.com/"


def create_account(name, password) -> bool:
    """Returns boolean value of a success"""
    data = {"Method": "Signup", "Username": name, "Password": password}
    r = requests.post(bluecoin_server, json=data)
    if r.status_code == 200:
        return True
    return False

def delete_account(name, password):
    data = {"Method": "DeleteAccount", "Username": name, "Password": password}
    r = requests.post(bluecoin_server, json=data)

def transfer(name, password, receiver, amount):
    data = {"ReceivingUser": receiver, "Password": password, "Username": name,
            "Amount": amount, "Method": "Transaction"}
    r = requests.post(bluecoin_server, json=data)


def balance(name, password):
    data = {"Username": name, "Password": password, "Method": "CheckBalance"}
    r = requests.post(bluecoin_server, json=data)
    return r.text


if __name__ == "__main__":
    pass