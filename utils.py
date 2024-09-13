import math

import numpy as np


def infer_integrated_data_layer(user_profile: dict) -> dict:
    # region Alcohol consumption
    alcohol_consumption = user_profile["alcohol"]
    if alcohol_consumption == 0:
        alcohol_consumption = 5
    elif alcohol_consumption <= 2:
        alcohol_consumption = 4
    elif alcohol_consumption <= 4:
        alcohol_consumption = 3
    elif alcohol_consumption <= 8:
        alcohol_consumption = 2
    elif alcohol_consumption <= 10:
        alcohol_consumption = 1

    user_profile["alcohol_consumption"] = [alcohol_consumption, 0.9]

    # endregion Alcohol consumption
    # region Stress level
    perceived_stress, _ = user_profile["perceived_stress"]
    recovery_during_24_hours, recovery_during_24_hours_confidence = user_profile["recovery_during_24_hours"]
    if recovery_during_24_hours_confidence <= 0.6:
        stress_level = perceived_stress
        confidence = 0.8
    else:
        stress_level = min(perceived_stress, recovery_during_24_hours)
        x_prime = min_max_transform(recovery_during_24_hours, 1, 5)
        y_prime = min_max_transform(perceived_stress, 1, 5)
        confidence = 1 - abs(x_prime - y_prime)

    user_profile["stress_level"] = [stress_level, confidence]
    # endregion Stress level
    # region Usage of tobacco products
    tobacco_products = user_profile["smoking"]
    user_profile["usage_of_tobacco_products"] = [tobacco_products, 0.8]
    # endregion Usage of tobacco products
    # region Strength of nicotine addiction
    usage_of_tobacco_products, _ = user_profile["usage_of_tobacco_products"]
    smoking_test = user_profile["smoking_test"]
    if usage_of_tobacco_products < 3:
        if smoking_test <= 1:
            strength_of_nicotine_addiction = 4
        elif smoking_test == 2:
            strength_of_nicotine_addiction = 3
        elif smoking_test == 3:
            strength_of_nicotine_addiction = 2
        elif smoking_test <= 6:
            strength_of_nicotine_addiction = 1
        else:
            raise ValueError(
                f"Smoking test should be between 0 and 6. Got {smoking_test} on {user_profile}")
    elif usage_of_tobacco_products >= 3:
        strength_of_nicotine_addiction = 5

    user_profile["strength_of_nicotine_addiction"] = [strength_of_nicotine_addiction, 0.9]
    # endregion Strength of nicotine addiction
    # region Vegetable Fruit Intake
    vegetable_fruit_consumption = user_profile["vegetables_fruits"]
    user_profile["vegetable_fruit_consumption"] = [vegetable_fruit_consumption, 0.8]
    # endregion Vegetable Fruit Intake
    # region Perceived physical activity level
    perceived_physical_activity_level = user_profile["perceived_physical_activity"]
    user_profile["perceived_physical_activity_level"] = [perceived_physical_activity_level, 0.8]
    # endregion Perceived physical activity level
    # region Exercise habits
    perceived_physical_activity_level, _ = user_profile["perceived_physical_activity_level"]
    physical_activity_level, physical_activity_level_confidence = user_profile["physical_activity_level"]
    if physical_activity_level_confidence <= 0.6:
        exercise_habits = perceived_physical_activity_level
        confidence = 0.8
    else:
        exercise_habits = round(np.mean([perceived_physical_activity_level, physical_activity_level]))
        x_prime = min_max_transform(physical_activity_level, 1, 5)
        y_prime = min_max_transform(perceived_physical_activity_level, 1, 5)
        confidence = 1 - abs(x_prime - y_prime)

    user_profile["exercise_habits"] = [exercise_habits, confidence]
    # endregion Exercise habits

    return user_profile


def infer_aggregated_data_layer(user_profile: dict) -> dict:
    return_dict = {}
    # region Improve Sleep Quality
    Xs = [user_profile["recovery_during_sleep"][0], user_profile["perceived_sleep_problems"][0],
          user_profile["recovery_during_24_hours"][0], user_profile["perceived_sleep_sufficiency"][0],
          user_profile["perceived_stress"][0], user_profile["stress_level"][0], user_profile["sleep_quality"][0]]
    xs = [min_max_transform(x, 1, 5) for x in Xs]
    ws = [6, 1, 3, 7, 3, 8, 10]
    assert len(Xs) == len(xs) == len(
        ws), f"Xs, xs and ws should have the same length. Got Xs: {len(Xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["improve_sleep_quality"] = [v, 4]
    # endregion Improve Sleep Quality
    # region Increase Physical Activity
    Xs = [user_profile["physical_activity_level"][0], user_profile["perceived_physical_activity_level"][0],
          user_profile["exercise_habits"][0]]
    xs = [min_max_transform(x, 1, 5) for x in Xs]
    ws = [8, 4, 8]
    assert len(Xs) == len(xs) == len(
        ws), f"Xs, xs and ws should have the same length. Got Xs: {len(Xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["increase_physical_activity"] = [v, 4]
    # endregion Increase Physical Activity
    # region Improve Diet Quality
    Xs = [user_profile["vegetable_fruit_consumption"][0], user_profile["excessive_intake_of_unhealthy_foods"][0],
          user_profile["eating_rhythm"][0], user_profile["emotional_eating"][0]]
    xs = [min_max_transform(x, 1, 5) for x in Xs]
    ws = [8, 8, 3, 3]
    assert len(Xs) == len(xs) == len(
        ws), f"Xs, xs and ws should have the same length. Got Xs: {len(Xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["improve_diet_quality"] = [v, 4]
    # endregion Improve Diet Quality
    # region Reduce Alcohol Consumption
    Xs = [user_profile["alcohol_consumption"][0]]
    xs = [min_max_transform(x, 1, 5) for x in Xs]
    ws = [10]
    assert len(Xs) == len(xs) == len(
        ws), f"Xs, xs and ws should have the same length. Got Xs: {len(Xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["reduce_alcohol_consumption"] = [v, 4]
    # endregion Reduce Alcohol Consumption
    # region Cease Smoking
    Xs = [user_profile["usage_of_tobacco_products"][0], user_profile["strength_of_nicotine_addiction"][0]]
    xs = [min_max_transform(x, 1, 5) for x in Xs]
    ws = [8, 10]
    assert len(Xs) == len(xs) == len(
        ws), f"Xs, xs and ws should have the same length. Got Xs: {len(Xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["cease_smoking"] = [v, 4]
    # endregion Cease Smoking
    return return_dict


def min_max_transform(x, x_min, x_max):
    return (x - x_min) / (x_max - x_min)


def normalized_manhattan_distance(xs, ws):
    return np.sum(ws * np.abs(np.ones(len(xs)) - xs)) / np.sum(ws)


def map_v_prime_to_v(v_prime):
    if v_prime < 0.125:
        return 1
    elif v_prime < 0.375:
        return 2
    elif v_prime < 0.625:
        return 3
    elif v_prime < 0.875:
        return 4
    else:
        return 5


def sim_need(user_profile: dict, intervention_library: dict):
    sim_need_dict = {}
    for intervention_title, intervention_properties in intervention_library.items():
        sim = 0
        intervention_operator = intervention_properties["opr"]

        # |b_str - 1|
        distances = []
        for behavior in intervention_properties["beh"]:
            if behavior in user_profile:
                distances.append(abs(user_profile[behavior][0] - 1))

        if intervention_operator == "min":
            sim = 1 - np.min(distances)
        elif intervention_operator == "max":
            sim = 1 - np.max(distances)
        elif intervention_operator == "weighted":
            raise NotImplementedError("Weighted operator is not implemented yet.")

        sim_need_dict[intervention_title] = sim

    return sim_need_dict


def sim_stage(user_profile: dict, intervention_library: dict):
    sim_stage_dict = {}
    for intervention_title, intervention_properties in intervention_library.items():
        relevant_behaviors_stages = []
        for behavior in intervention_properties["beh"]:
            if behavior in user_profile:
                relevant_behaviors_stages.append(user_profile[behavior][1])

        for stage in intervention_properties["stg"]:
            if stage in relevant_behaviors_stages:
                sim_stage_dict[intervention_title] = 1.0

        min_distance = math.inf
        if intervention_title not in sim_stage_dict:
            for i in relevant_behaviors_stages:
                for j in intervention_properties["stg"]:
                    if abs(i - j) < min_distance:
                        min_distance = abs(i - j)
            sim_stage_dict[intervention_title] = 1 - 0.25 * min_distance

    return sim_stage_dict


def sim_total(sim_needs, sim_stages):
    sim_total_dict = {}
    for intervention_title in sim_needs:
        if sim_needs[intervention_title] >= 0.5:
            sim_total_dict[intervention_title] = 0.5 * sim_needs[intervention_title] + 0.5 * sim_stages[
                intervention_title]
        else:
            sim_total_dict[intervention_title] = 0

    return sim_total_dict