import random

user_profile = {}
user_profile["missing_heart_rate_percentage_vector"] = [random.randint(0, 100) for _ in range(3)]
user_profile["recovery_during_sleep_vector"] = [random.randint(0, 100) for _ in range(3)]
user_profile["recovery_during_day_vector"] = [random.randint(0, 30) for _ in range(3)]
user_profile["perceived_sleep_problems"] = random.randint(1, 5)
user_profile["perceived_sleep_sufficiency"] = random.randint(1, 5)
user_profile["perceived_stress"] = random.randint(1, 5)
user_profile["physical_activity_points_vector"] = [random.randint(0, 100) for _ in range(3)]
user_profile["perceived_physical_activity"] = random.randint(1, 5)
user_profile["vegetables_fruits"] = random.randint(1, 5)
user_profile["fast_food"] = random.randint(1, 5)
user_profile["eating_rhythm"] = random.randint(1, 5)
user_profile["emotional_eating"] = random.randint(1, 5)
user_profile["alcohol"] = random.randint(0, 10)
user_profile["smoking"] = random.randint(1, 5)
user_profile["smoking_test"] = random.randint(0, 6)

import requests

url = f"http://localhost:8000/"
response = requests.post(url, json=user_profile)

print(response.json())