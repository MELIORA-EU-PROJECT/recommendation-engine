import requests
import json5

# url = f"https://datacollection.risa.eu/onboarding/onboardingQuestionnaire/all"
# url = f"http://144.76.87.115:5004/v1/api/motivational-tips"
url = f"http://localhost:8000/v2/physical_activity_level/"
users = ["EL498546TEST", "EL731238TEST", "EL122068TEST", "EL488249TEST", "EL935243TEST", "EL333170TEST", "EL553569TEST",
		 "EL603224TEST"]
headers = {
	"Authorization": "Basic bWVsaW9yYTpqeEtFd08wVjR2N2kweG8="
}

for user in users:
	print(f"User: {user}")
	response = requests.get(url + user, headers=headers)
	res = response.json()
	print(f"Status code: {response.status_code}")
	print(f"Res: {json5.dumps(res, indent=4, quote_keys=True)}")