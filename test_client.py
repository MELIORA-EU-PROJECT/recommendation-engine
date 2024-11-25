import json5
import requests

# url = f"http://localhost:1564/"
url = f"http://144.76.87.115:1564/debug_recommend"

# with open("example_patients/alcohol_physical.json", "r") as f:
# with open("example_patients/sim_stage_showcase.json", "r") as f:
with open("example_patients/single_physical.json", "r") as f:
    data = json5.load(f)
    print(f"Sending data: {json5.dumps(data, indent=4, quote_keys=True)}")
    response = requests.post(url, json=data)  # json=json5.loads(data))
    print(f"Response:")
    print(json5.dumps(response.json(), indent=4, quote_keys=True))