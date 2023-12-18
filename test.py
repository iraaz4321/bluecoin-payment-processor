import requests
json_data = {"amount": 200, "redirect_url": "https://google.com/"}
r = requests.post("http://127.0.0.1:8000/api/payment/", json=json_data)
print(r.json())