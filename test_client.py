import json5
import requests

url = f"http://localhost:8000/"

data = "Nikos"
print(f"Sending data: {data}")
response = requests.post(url, json={"onoma": data})  # json=json5.loads(data))

print(response.json())