"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""
from typing import Dict, Any

import json5
from utils import *

# @formatter:off
# TODO: Add more items
intervention_library = {"Twitter_Post_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [1,2,3], "opr": "max"},
                        "Youtube_Video_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [2,3], "opr": "max"},
                        "News_Article_About_Diet_And_Exercise": {"beh": ["improve_diet_quality", "increase_physical_activity"], "stg": [2, 3], "opr": "min"},
                        "Facebook_Post_About_Getting_Better_Sleep": {"beh": ["improve_sleep_quality"], "stg": [4,5], "opr": "max"},
                        "Instagram_Reel_About_Reducing_Alcohol_Intake": {"beh": ["reduce_alcohol_consumption"], "stg": [2,3,4], "opr": "max"},
                        "TikTok_About_Reducing_Alcohol_Intake": {"beh": ["reduce_alcohol_consumption"], "stg": [5], "opr": "max"},
                        "Youtube_Short_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [1,2], "opr": "max"},
                        "Youtube_Video_About_Improving_Life_Quality": {"beh": ["cease_smoking","reduce_alcohol_consumption","improve_diet_quality","increase_physical_activity","improve_sleep_quality"], "stg": [1,2,3], "opr": "min"},}
# @formatter:on

def get_recommendations(user_profile) -> dict:
    # with open("example_patient.json", "r") as read_file:
    #     user_profile = json5.load(read_file)
    user_profile = infer_integrated_data_layer(user_profile)
    with open("example_patient_integrated.json", "w") as write_file:
        json5.dump(user_profile, write_file, indent=4, quote_keys=True)
    user_profile = infer_aggregated_data_layer(user_profile)
    with open("example_patient_aggregated.json", "w") as write_file:
        json5.dump(user_profile, write_file, indent=4, quote_keys=True)
    user_profile = {k: [min_max_transform(v[0], 1, 5), v[1]]
                    for k, v in user_profile.items()}
    sim_needs = sim_need(user_profile, intervention_library)
    sim_stages = sim_stage(user_profile, intervention_library)
    sim_totals = sim_total(sim_needs, sim_stages)
    # print(f"Similarity Needs: {sim_needs}")
    # print("-" * 50)
    # print(f"Similarity Stages: {sim_stages}")
    # print("-" * 50)
    # print(f"Similarity Totals: {sim_totals}")
    # print("-" * 50)

    sim_totals_filtered = {k: v for k, v in sim_totals.items() if v >= 0.5}
    # print(f"Similarity Totals Filtered (if value >= 0.5): {sim_totals_filtered}")
    # print("-" * 50)

    sim_total_ordered = dict(sorted(sim_totals_filtered.items(), key=lambda x: x[1], reverse=True))
    # print(f"Similarity Totals Filtered and Ordered: {sim_total_ordered}")
    return sim_total_ordered


from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


class UserProfile(BaseModel):
    missing_heart_rate_percentage_vector: list[int]
    recovery_during_sleep_vector: list[int]
    recovery_during_day_vector: list[int]
    perceived_sleep_problems: int
    perceived_sleep_sufficiency: int
    perceived_stress: int
    physical_activity_points_vector: list[int]
    perceived_physical_activity: int
    vegetables_fruits: int
    fast_food: int
    eating_rhythm: int
    emotional_eating: int
    alcohol: int
    smoking: int
    smoking_test: int


@app.post("/")
async def root(item: UserProfile):
    user_profile = item.model_dump()
    print(f"User Profile: {user_profile}")
    recommendations = get_recommendations(user_profile)
    return recommendations