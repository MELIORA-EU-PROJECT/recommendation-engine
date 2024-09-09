import random
import numpy as np

user_profile = {}
# TODO:
# bernouli distributions
# lognormal distributions
# uniform distributions
# READ TTM
# add more examples

# region Missing Heart Rate Percentage Vector - Lognormal Distribution
distribution = np.random.lognormal(0, 1, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 100)
distribution = distribution.astype(int)
user_profile["missing_heart_rate_percentage_vector"] = np.random.choice(distribution)
# endregion
# region Recovery During Sleep Vector - Normal Distribution (With Random Mean - 10 to 91 Uniform Distribution)
patient_rand = random.randint(10, 91)
distribution = np.random.normal(patient_rand, 5, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 100)
distribution = distribution.astype(int)
user_profile["recovery_during_sleep_vector"] = np.random.choice(distribution, 3)
# endregion
# region Recovery During Day Vector - Normal Distribution (With Random Mean - 10 to 20 Uniform Distribution)
patient_rand = random.randint(10, 20)
distribution = np.random.normal(patient_rand, 2, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 30)
distribution = distribution.astype(int)
user_profile["recovery_during_day_vector"] = np.random.choice(distribution, 3)
# endregion
# region Perceived Sleep Problems - Uniform Distribution
user_profile["perceived_sleep_problems"] = random.randint(1, 5)
# endregion
# region Perceived Sleep Sufficiency - Uniform Distribution
user_profile["perceived_sleep_sufficiency"] = random.randint(1, 5)
# endregion
# region Perceived Stress - Uniform Distribution
user_profile["perceived_stress"] = random.randint(1, 5)
# endregion
# region Physical Activity Points Vector - Normal Distribution (With Random Mean - 10 to 91 Uniform Distribution)
patient_rand = random.randint(10, 91)
distribution = np.random.normal(patient_rand, 5, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 100)
distribution = distribution.astype(int)
user_profile["physical_activity_points_vector"] = np.random.choice(distribution, 3)
# endregion
# region Perceived Physical Activity - Uniform Distribution
user_profile["perceived_physical_activity"] = random.randint(1, 5)
# endregion
# region Vegetables Fruits - Normal Distribution
distribution = np.random.normal(3, 1, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 1, 5)
distribution = distribution.astype(int)
user_profile["vegetables_fruits"] = np.random.choice(distribution)
# endregion
# region Fast Food - Inverse Lognormal Distribution
distribution = np.random.lognormal(3.6, 0.6, 1000)
distribution = np.clip(distribution, 0, 100)
distribution = -distribution
distribution = distribution + 100
distribution = np.round(distribution)
distribution = distribution / (100 / 5)
distribution = distribution.astype(int)
user_profile["fast_food"] = np.random.choice(distribution) + 1
# endregion
# region Eating Rhythm & Emotional Eating - Normal Distribution
distribution = np.random.normal(2.5, 1.7, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 5)
distribution = distribution.astype(int)
user_profile["eating_rhythm"] = np.random.choice(distribution)
user_profile["emotional_eating"] = np.random.choice(distribution)
# endregion
# region Alcohol - Normal Distribution
distribution = np.random.normal(5, 2, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 10)
distribution = distribution.astype(int)
user_profile["alcohol"] = np.random.choice(distribution)
# endregion
# region Smoking - Normal Distribution
distribution = np.random.normal(2.5, 1.7, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 5)
distribution = distribution.astype(int)
user_profile["smoking"] = np.random.choice(distribution)
# endregion
# region Smoking Test - Normal Distribution
distribution = np.random.normal(3, 1.4, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 6)
distribution = distribution.astype(int)
user_profile["smoking_test"] = np.random.choice(distribution)
# endregion

# TODO PAPER
# RELATED WORK + INTRO
# 4 PAPERS ON CAUSALITY
# CREATE A DUMMY GRAPH AND TRY TO INTEGRATE IT IN THE PROGRAM
# DOWHY framework,GraphViz,
# write a simple explantation of dag integration in the TTM
import requests

url = f"http://localhost:8000/"
response = requests.post(url, json=user_profile)

print(response.json())