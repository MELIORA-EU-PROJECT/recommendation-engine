import json5
import requests

url = f"http://localhost:8000/"

with open("example_patients/alcohol_physical.json", "r") as f:
    data = json5.load(f)
    print(f"Sending data: {json5.dumps(data, indent=4, quote_keys=True)}")
    response = requests.post(url, json=data)  # json=json5.loads(data))
    print(f"Response:")
    print(json5.dumps(response.json(), indent=4, quote_keys=True))