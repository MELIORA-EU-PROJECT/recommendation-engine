import json5
import requests

url = f"http://localhost:8000/"

data = """
{
  "missing_heart_rate_percentage_vector": [
    4,
    0,
    2
  ],
  "recovery_during_sleep_vector": [
    57,
    29,
    91
  ],
  "recovery_during_day_vector": [
    20,
    13,
    25
  ],
    "perceived_sleep_problems": 3,
    "perceived_sleep_sufficiency": 4,
    "perceived_stress": 2,
    "physical_activity_points_vector": [
    100,
    34,
    76
  ],
    "perceived_physical_activity": 4,
    "vegetables_fruits": 3,
    "fast_food": 2,
    "eating_rhythm": 3,
    "emotional_eating": 2,
    "alcohol": 3,
    "smoking": 2,
    "smoking_test": 5
}
"""
response = requests.post(url, json=json5.loads(data))

print(response.json())