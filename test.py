import requests
json_data = {"amount": 0.0001, "redirect_url": "https://google.com/", "receiver": "iraas"}
r = requests.post("http://127.0.0.1:8000/api/payment/", json=json_data)

#json_data = {"account": "IzC3c4lawTtvNjin"}
#r = requests.post("http://127.0.0.1:8000/api/payment_state/", json=json_data)
print(r.text)
print(r.json())