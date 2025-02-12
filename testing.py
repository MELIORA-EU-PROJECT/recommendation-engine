import requests
import json5

from dotenv import load_dotenv

import utils
from utils import create_user_profile

import numpy as np
import matplotlib.pyplot as plt

# url = f"https://datacollection.risa.eu/onboarding/onboardingQuestionnaire/all"
url = f"https://datacollection.risa.eu/onboarding/participantsBaseline/all"
headers = {
	"Authorization": "Basic bWVsaW9yYTpqeEtFd08wVjR2N2kweG8="
}

response = requests.get(url, headers=headers)
tips = response.json()
print(f"Tips length: {len(tips)}")
print(f"Tips: {json5.dumps(tips, indent=4, quote_keys=True)}")
with open("scrap/tips.json", "w") as f:
	json5.dump(tips, f, indent=4, quote_keys=True)
# response = requests.get(url_ids, headers=headers)
# question_ids = response.json()
# for q in question_ids:
#     print(f"if \"{q}\" in temp_user_profile:\n    if temp_user_profile[\"{q}\"] is not None:")