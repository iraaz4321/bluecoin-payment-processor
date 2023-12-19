import requests
"""json_data = {"amount": 200, "redirect_url": "https://google.com/", "receiver": "iraaz"}
r = requests.post("http://127.0.0.1:8000/api/payment/", json=json_data)"""

json_data = {"account": "IzC3c4lawTtvNjin"}
r = requests.post("http://127.0.0.1:8000/api/payment_state/", json=json_data)
print(r.text)
print(r.json())