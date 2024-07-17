from ExtraDataClasses import CancerData
from UserProfile import UserProfile

user_profiles = [
    UserProfile(60, "White", 3, 3, 3, 1.75, 80, 3, 3, 3, 3, CancerData(True, 60, "Chemotherapy", "2021-01-01"), ), ]

rules = {
    "age > 50": lambda user: user.age > 50,
    "Has cancer": lambda user: user.status is not None and user.status.active,
    "Ethnicity is White": lambda user: user.ethnicity == "White",
    "Economic level is 3": lambda user: user.economic_level == 3,
    "Has medical conditions": lambda user: user.medical_conditions is not None and len(
        user.medical_conditions) > 0,
    "Has mental conditions": lambda user: user.mental_conditions is not None and len(user.mental_conditions) > 0,
    "BMI > 25": lambda user: user.weight / (user.height ** 2) > 25,
}

rules_met = {rule: False for rule in rules.keys()}

user_profile = user_profiles[0]

for rule, condition in rules.items():
    rules_met[rule] = condition(user_profile)

print(rules_met)