import requests
import json5

from utils import create_user_profile

# url = "https://datacollection.risa.eu/onboarding/participantsBaseline/all"
create_user_profile("EL553569TEST")

# url_ids = "https://datacollection.risa.eu/onboarding/onboardingQuestionnaire/ids"
#
# headers = {
#     "Authorization": "Basic bWVsaW9yYTpqeEtFd08wVjR2N2kweG8="
# }
#
# response = requests.get(url_ids, headers=headers)
# question_ids = response.json()
# for q in question_ids:
#     print(f"if \"{q}\" in temp_user_profile:\n    if temp_user_profile[\"{q}\"] is not None:")