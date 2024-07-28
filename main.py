"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""

import json5
from utils import *

# @formatter:off
intervention_library = {"Twitter_Post_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [4], "opr": "max"},
                        "Youtube_Video_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [2], "opr": "max"},
                        "News_Article_About_Diet_And_Exercise": {"beh": ["improve_diet_quality", "increase_physical_activity"], "stg": [2, 3], "opr": "min"},
                        "Facebook_Post_About_Getting_Better_Sleep": {"beh": ["improve_sleep_quality"], "stg": [5], "opr": "max"},
                        "Instagram_Reel_About_Reducing_Alcohol_Intake": {"beh": ["reduce_alcohol_consumption"], "stg": [3], "opr": "max"},
                        "TikTok_About_Reducing_Alcohol_Intake": {"beh": ["reduce_alcohol_consumption"], "stg": [5], "opr": "max"},
                        "Youtube_Short_About_Quiting_Smoking": {"beh": ["cease_smoking"], "stg": [1], "opr": "max"},
                        "Youtube_Video_About_Improving_Life_Quality": {"beh": ["cease_smoking","reduce_alcohol_consumption","improve_diet_quality","increase_physical_activity","improve_sleep_quality"], "stg": [1, 1, 1, 1, 1], "opr": "min"},}
# @formatter:on

with open("example_patient.json", "r") as read_file:
    user_profile = json5.load(read_file)
user_profile = infer_integrated_data_layer(user_profile)
with open("example_patient_integrated.json", "w") as write_file:
    json5.dump(user_profile, write_file, indent=4, quote_keys=True)
user_profile = infer_aggregated_data_layer(user_profile)
with open("example_patient_aggregated.json", "w") as write_file:
    json5.dump(user_profile, write_file, indent=4, quote_keys=True)
user_profile = {k: [min_max_transform(v[0], 1, 5), v[1]]
                for k, v in user_profile.items()}
sim_needs = sim_need(user_profile, intervention_library)
print(sim_needs)