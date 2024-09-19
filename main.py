"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""
import logging

import json5
import uvicorn
from utils import *

# @formatter:off
# TODO: Add more items
intervention_library = {"Twitter_Post_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [1,2,3], "opr": "max"},
                        "Youtube_Video_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [2,3], "opr": "max"},
                        "News_Article_About_Diet_And_Exercise": {"beh": ["improve_diet_quality", "increase_physical_activity"], "stg": [2, 3], "opr": "min"},
                        "Instagram_Reel_About_Reducing_Alcohol_Intake": {"beh": ["reduce_alcohol_consumption"], "stg": [2,3,4], "opr": "max"},
                        "TikTok_About_Reducing_Alcohol_Intake": {"beh": ["reduce_alcohol_consumption"], "stg": [5], "opr": "max"},
                        "Youtube_Short_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [1,2], "opr": "max"},
                        "Youtube_Video_About_Improving_Life_Quality": {"beh": ["cease_smoking","reduce_alcohol_consumption","improve_diet_quality","increase_physical_activity","improve_mental_health"], "stg": [1,2,3], "opr": "min"},}
# @formatter:on

def diff_user_profile(new_user_profile: dict, old_user_profile: dict) -> dict:
    return_dict = {}
    for new_key, new_value in new_user_profile.items():
        if new_key in old_user_profile:
            if new_value != old_user_profile[new_key]:
                return_dict[new_key] = new_value
        else:
            return_dict[new_key] = new_value

    return return_dict


from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/")
async def root(item: Request):
    user_profile = await item.json()

    print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
    # Integrated Data Layer
    old_user_profile = user_profile.copy()
    user_profile = infer_integrated_data_layer(user_profile)
    with open("example_patient_integrated.json", "w") as write_file:
        json5.dump(user_profile, write_file, indent=4, quote_keys=True)
    print(f"Integrated Data Layer: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
    # Diff User Profile
    integrated_layer_profile = diff_user_profile(user_profile, old_user_profile)
    print(f"Diff User Profile: {json5.dumps(integrated_layer_profile, indent=4, quote_keys=True)}")
    # Aggregated Data Layer
    old_user_profile = user_profile
    user_profile = infer_aggregated_data_layer(user_profile)
    with open("example_patient_aggregated.json", "w") as write_file:
        json5.dump(user_profile, write_file, indent=4, quote_keys=True)
    print(f"Aggregated Data Layer: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
    # Diff User Profile
    agregated_layer_profile = diff_user_profile(user_profile, old_user_profile)
    print(f"Diff User Profile: {json5.dumps(agregated_layer_profile, indent=4, quote_keys=True)}")
    # TTM stages
    old_user_profile = user_profile
    ttm_user_profile = add_ttm_stages(user_profile)
    with open("example_patient_ttm.json", "w") as write_file:
        json5.dump(ttm_user_profile, write_file, indent=4, quote_keys=True)
    print(f"TTM Stages: {json5.dumps(ttm_user_profile, indent=4, quote_keys=True)}")
    # Diff User Profile
    ttm_layer_profile = diff_user_profile(ttm_user_profile, old_user_profile)
    print(f"Diff User Profile: {json5.dumps(ttm_layer_profile, indent=4, quote_keys=True)}")
    # Similarity Needs
    ttm_user_profile = {k: {"str": min_max_transform(v["str"], 1, 5), "stg": v["stg"]}
                        for k, v in ttm_user_profile.items()}
    sim_needs = sim_need(ttm_user_profile, intervention_library)
    sim_stages = sim_stage(ttm_user_profile, intervention_library)
    sim_totals = sim_total(sim_needs, sim_stages)
    sim_totals_filtered = {k: v for k, v in sim_totals.items() if v >= 0.5}
    sim_total_ordered = dict(sorted(sim_totals_filtered.items(), key=lambda x: x[1], reverse=True))
    return {"recommendations": sim_total_ordered, "user_profile": ttm_user_profile,
            "diffs": {"integrated": integrated_layer_profile, "aggregated": agregated_layer_profile,
                      "ttm": ttm_layer_profile}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)