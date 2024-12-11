import json5
import requests

import data_generator


def get_most_important_behaviour_change_need(aggregate_profile: dict):
    max_v = 0
    for v in aggregate_profile.values():
        max_v = max(max_v, v["str"])

    rv = []
    for k, v in aggregate_profile.items():
        if v["str"] == max_v:
            rv.append(k)

    return rv


def check_matching_recommendations(behaviours: list, recommendations: dict):
    total_recs = 0
    matching_recs = 0
    for v in recommendations.values():
        total_recs += 1
        for behaviour in behaviours:
            if behaviour in v["goals"]:
                matching_recs += 1
                break

    return total_recs, matching_recs


url = f"http://144.76.87.115:1564/debug_recommend"
number_of_profiles = 1000
total_recommendations = 0
matching_recommendations = 0
i = 0
while i < number_of_profiles:
    user_profile = data_generator.generate_user_profile()
    # print(f"Profile {i}: {user_profile}")
    response = requests.post(url, json=user_profile)

    json_response = response.json()
    print(f"Response {i}: {json5.dumps(json_response, indent=4, quote_keys=True)}")

    behaviour = get_most_important_behaviour_change_need(json_response["user_profile"])
    print(f"Behaviour {i}: {behaviour}")

    # if len(behaviour) > 3:
    #     print(f"Too many behaviours, inconsistent profile gen. Regenerating profile {i}")
    #     continue

    number_of_recs, matching_recs = check_matching_recommendations(behaviour, json_response["recommendations"])
    print(f"Matching Recommendations {i}: {matching_recs}/{number_of_recs}")

    total_recommendations += number_of_recs
    matching_recommendations += matching_recs

    with open(f"evaluation_res/profiles/profile_{i}.json", "w") as f:
        json5.dump(user_profile, f, indent=4, quote_keys=True)

    with open(f"evaluation_res/responses/response_{i}.json", "w") as f:
        json5.dump(json_response, f, indent=4, quote_keys=True)

    i += 1

print(f"Total Recommendations: {total_recommendations}")
print(f"Matching Recommendations: {matching_recommendations}")
print(f"Matching Recommendations Ratio: {matching_recommendations / total_recommendations}")