"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""

import json5
from utils import *

with open("example_patient.json", "r") as read_file:
    user_profile = json5.load(read_file)
    user_profile = infer_integrated_data_layer(user_profile)
    user_profile = infer_aggregated_data_layer(user_profile)
    print(json5.dumps(user_profile, indent=4))