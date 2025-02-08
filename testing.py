import requests
import json5

from dotenv import load_dotenv

import utils
from utils import create_user_profile

import numpy as np
import matplotlib.pyplot as plt

url = f"http://144.76.87.115:5004/v1/api/tips"
headers = {
	"Authorization": "Basic bWVsaW9yYTpqeEtFd08wVjR2N2kweG8="
}

# full_url = f"{url}?language=English"
full_url = f"{url}?user_level=beginner"
print(f"Full URL: {full_url}")
response = requests.get(full_url, headers=headers)
tips = response.json()
print(f"Tips length: {len(tips)}")
print(f"Tips: {json5.dumps(tips, indent=4, quote_keys=True)}")
# response = requests.get(url_ids, headers=headers)
# question_ids = response.json()
# for q in question_ids:
#     print(f"if \"{q}\" in temp_user_profile:\n    if temp_user_profile[\"{q}\"] is not None:")