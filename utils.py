import math

import numpy as np


def infer_integrated_data_layer(user_profile: dict) -> dict:
    # region Alcohol consumption
    how_often_alcohol = user_profile["how_often_alcohol"]
    match how_often_alcohol:
        case "never":
            how_often_alcohol = 5
        case "monthly or less":
            how_often_alcohol = 4
        case "2-4 times per month":
            how_often_alcohol = 3
        case "2-3 times per week":
            how_often_alcohol = 2
        case "4 or more times per week":
            how_often_alcohol = 1
        case _:
            raise ValueError(f"how_often_alcohol should be one of the following: "
                             f"never, monthly or less, 2-4 times per month, 2-3 times per week, 4 or more times per week. "
                             f"On {user_profile} got {how_often_alcohol}")

    drinks_per_session = user_profile["drinks_per_session"]
    match drinks_per_session:
        case "1-2":
            drinks_per_session = 5
        case "3-4":
            drinks_per_session = 4
        case "5-6":
            drinks_per_session = 3
        case "7-9":
            drinks_per_session = 2
        case "10 or more":
            drinks_per_session = 1
        case _:
            raise ValueError(f"drinks_per_session should be one of the following: "
                             f"10 or more, 7-9, 5-6, 3-4, 1-2. "
                             f"On {user_profile} got {drinks_per_session}")

    how_often_6_or_more_drinks = user_profile["how_often_6_or_more_drinks"]
    match how_often_6_or_more_drinks:
        case "never":
            how_often_6_or_more_drinks = 5
        case "less than monthly":
            how_often_6_or_more_drinks = 4
        case "monthly":
            how_often_6_or_more_drinks = 3
        case "weekly":
            how_often_6_or_more_drinks = 2
        case "daily or almost daily":
            how_often_6_or_more_drinks = 1
        case _:
            raise ValueError(f"how_often_6_or_more_drinks should be one of the following: "
                             f"never, less than monthly, monthly, weekly, daily or almost daily. "
                             f"On {user_profile} got {how_often_6_or_more_drinks}")

    alcohol_last_week = user_profile["alcohol_last_week"]

    match alcohol_last_week:
        case "none":
            alcohol_last_week = 5
        case "1":
            alcohol_last_week = 4
        case "2-3":
            alcohol_last_week = 3
        case "4 or more":
            alcohol_last_week = 1
        case _:
            raise ValueError(f"alcohol_last_week should be one of the following: "
                             f"none, 1, 2-3, 4 or more. "
                             f"On {user_profile} got {alcohol_last_week}")

    alcohol_last_week_per_day = user_profile["alcohol_last_week_per_day"]
    match alcohol_last_week_per_day:
        case "1-2":
            alcohol_last_week_per_day = 5
        case "3-4":
            alcohol_last_week_per_day = 4
        case "5-6":
            alcohol_last_week_per_day = 3
        case "7-9":
            alcohol_last_week_per_day = 2
        case "10 or more":
            alcohol_last_week_per_day = 1
        case _:
            raise ValueError(f"alcohol_last_week_per_day should be one of the following: "
                             f"10 or more, 7-9, 5-6, 3-4, 1-2. "
                             f"On {user_profile} got {alcohol_last_week_per_day}")

    alcohol_6_or_more_single_occasions = user_profile["alcohol_6_or_more_single_occasions"]
    match alcohol_6_or_more_single_occasions:
        case "none":
            alcohol_6_or_more_single_occasions = 5
        case "1":
            alcohol_6_or_more_single_occasions = 4
        case "2-3":
            alcohol_6_or_more_single_occasions = 3
        case "4-5":
            alcohol_6_or_more_single_occasions = 2
        case "daily or almost daily":
            alcohol_6_or_more_single_occasions = 1
        case _:
            raise ValueError(f"alcohol_6_or_more_single_occasions should be one of the following: "
                             f"none, 1, 2-3, 4-5, daily or almost daily. "
                             f"On {user_profile} got {alcohol_6_or_more_single_occasions}")

    user_profile["alcohol_consumption"] = round(np.mean(
        [how_often_alcohol, drinks_per_session, how_often_6_or_more_drinks, alcohol_last_week,
         alcohol_last_week_per_day, alcohol_6_or_more_single_occasions]))

    # endregion Alcohol consumption
    # region Stress level
    # endregion Stress level
    # region Usage of tobacco products
    ever_smoked = user_profile["ever_smoked"]
    match ever_smoked:
        case "never":
            ever_smoked = 5
        case ">= 10 years":
            ever_smoked = 4
        case "< 10 years":
            ever_smoked = 3
        case "active":
            ever_smoked = 1
        case _:
            raise ValueError(f"ever_smoked should be one of the following: "
                             f"never, >= 10 years, < 10 years, active. "
                             f"On {user_profile} got {ever_smoked}")

    duration_of_smoking = user_profile["duration_of_smoking"]
    match duration_of_smoking:
        case "< 1 year":
            duration_of_smoking = 5
        case "2-5 years":
            duration_of_smoking = 4
        case "6-10 years":
            duration_of_smoking = 3
        case ">10":
            duration_of_smoking = 1
        case _:
            raise ValueError(f"duration_of_smoking should be one of the following: "
                             f"< 1 year, 2-5 years, 6-10 years, >10. "
                             f"On {user_profile} got {duration_of_smoking}")

    manufactured_cigarettes = user_profile["manufactured_cigarettes"]
    match manufactured_cigarettes:
        case 0:
            manufactured_cigarettes = 5
        case num if 1 <= num <= 2:
            manufactured_cigarettes = 4
        case num if 3 <= num <= 5:
            manufactured_cigarettes = 3
        case num if 6 <= num <= 10:
            manufactured_cigarettes = 2
        case num if num >= 11:
            manufactured_cigarettes = 1
        case _:
            raise ValueError(f"UNREACHABLE: manufactured_cigarettes: {manufactured_cigarettes}")

    hand_rolled_cigarettes = user_profile["hand_rolled_cigarettes"]
    match hand_rolled_cigarettes:
        case 0:
            hand_rolled_cigarettes = 5
        case num if 1 <= num <= 2:
            hand_rolled_cigarettes = 4
        case num if 3 <= num <= 5:
            hand_rolled_cigarettes = 3
        case num if 6 <= num <= 10:
            hand_rolled_cigarettes = 2
        case num if num >= 11:
            hand_rolled_cigarettes = 1
        case _:
            raise ValueError(f"UNREACHABLE: hand_rolled_cigarettes: {hand_rolled_cigarettes}")

    pipes = user_profile["pipes"]
    match pipes:
        case 0:
            pipes = 5
        case num if 1 <= num <= 2:
            pipes = 4
        case num if 3 <= num <= 5:
            pipes = 3
        case num if 6 <= num <= 10:
            pipes = 2
        case num if num >= 11:
            pipes = 1
        case _:
            raise ValueError(f"UNREACHABLE: pipes: {pipes}")

    cigars = user_profile["cigars"]
    match cigars:
        case 0:
            cigars = 5
        case 1:
            cigars = 4
        case 2:
            cigars = 3
        case 3:
            cigars = 2
        case num if num >= 4:
            cigars = 1
        case _:
            raise ValueError(f"UNREACHABLE: cigars: {cigars}")

    water_pipe = user_profile["water_pipe"]
    match water_pipe:
        case 0:
            water_pipe = 5
        case num if 1 <= num <= 2:
            water_pipe = 4
        case num if 3 <= num <= 5:
            water_pipe = 3
        case num if 6 <= num <= 10:
            water_pipe = 2
        case num if num >= 11:
            water_pipe = 1
        case _:
            raise ValueError(f"UNREACHABLE: water_pipe: {water_pipe}")

    other_tobacco_products = user_profile["other_tobacco_products"]
    match other_tobacco_products:
        case 0:
            other_tobacco_products = 5
        case num if 1 <= num <= 2:
            other_tobacco_products = 4
        case num if 3 <= num <= 5:
            other_tobacco_products = 3
        case num if 6 <= num <= 10:
            other_tobacco_products = 2
        case num if num >= 11:
            other_tobacco_products = 1
        case _:
            raise ValueError(f"UNREACHABLE: other_tobacco_products: {other_tobacco_products}")

    user_profile["usage_of_tobacco_products"] = round(np.mean(
        [ever_smoked, duration_of_smoking, manufactured_cigarettes, hand_rolled_cigarettes, pipes, cigars, water_pipe,
         other_tobacco_products]))
    # endregion Usage of tobacco products
    # region Eating Pyramid score
    # https://en.wikipedia.org/wiki/File:USDA_Food_Pyramid.gif
    serving_scale = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                     "3-4 servings per week", "5-6 servings per week", "1 serving per day", "2-3 servings per day",
                     "4-5 servings per day", "6 or more servings per day"]
    # 6 + 7 + 6 + 6 + 8 + 8 + 6 + 5 + 6 = 58

    _3_or_more_red_meat_weekly = user_profile["3_or_more_red_meat_weekly"]
    how_often_fruit = user_profile["how_often_fruit"]
    how_often_fruit = abs(serving_scale.index(how_often_fruit) - serving_scale.index("2-3 servings per day"))

    how_often_vegetables = user_profile["how_often_vegetables"]
    how_often_vegetables = abs(serving_scale.index(how_often_vegetables) - serving_scale.index("4-5 servings per day"))

    how_often_nuts = user_profile["how_often_nuts"]
    how_often_nuts = abs(serving_scale.index(how_often_nuts) - serving_scale.index("2-3 servings per day"))

    how_often_fish = user_profile["how_often_fish"]
    how_often_fish = abs(serving_scale.index(how_often_fish) - serving_scale.index("2-3 servings per day"))

    how_often_whole_grain = user_profile["how_often_whole_grain"]
    how_often_whole_grain = abs(
        serving_scale.index(how_often_whole_grain) - serving_scale.index("6 or more servings per day"))

    how_often_refined_grain = user_profile["how_often_refined_grain"]
    how_often_refined_grain = abs(
        serving_scale.index(how_often_refined_grain) - serving_scale.index("6 or more servings per day"))

    how_often_low_fat_dairy = user_profile["how_often_low_fat_dairy"]
    how_often_low_fat_dairy = abs(
        serving_scale.index(how_often_low_fat_dairy) - serving_scale.index("2-3 servings per day"))

    how_often_high_fat_dairy = user_profile["how_often_high_fat_dairy"]
    how_often_high_fat_dairy = serving_scale.index(how_often_high_fat_dairy) - serving_scale.index(
        "3-4 servings per week")

    how_often_sweets = user_profile["how_often_sweets"]
    how_often_sweets = serving_scale.index(how_often_sweets) - serving_scale.index("1-2 servings per week")

    aggregate_distances = how_often_fruit + how_often_vegetables + how_often_nuts + how_often_fish + how_often_whole_grain + how_often_refined_grain + how_often_low_fat_dairy + how_often_high_fat_dairy + how_often_sweets
    match aggregate_distances:
        case num if num <= 11:
            aggregate_distances = 5
        case num if 12 <= num <= 22:
            aggregate_distances = 4
        case num if 23 <= num <= 33:
            aggregate_distances = 3
        case num if 34 <= num <= 44:
            aggregate_distances = 2
        case num if num >= 45:
            aggregate_distances = 1
        case _:
            raise ValueError(f"UNREACHABLE: aggregate_distances: {aggregate_distances}")

    user_profile["eating_pyramid_score"] = aggregate_distances

    # endregion Eating Pyramid score
    # region Proximity to exercise facilities
    # endregion Proximity to exercise facilities
    # region Exercise habits
    # endregion Exercise habits
    # region Physical activity level
    # region vigorous activity
    # https://www.ncbi.nlm.nih.gov/books/NBK566048/
    if "vigorous_days_per_week" in user_profile:
        vigorous_days_per_week = user_profile["vigorous_days_per_week"]
        vigorous_time_per_day = user_profile["vigorous_time_per_day"]
        if vigorous_time_per_day is list:
            vigorous_time_per_day, time_unit = vigorous_time_per_day
            if time_unit == "hour":
                vigorous_time_per_day = vigorous_time_per_day * 60

            vigorous_time_per_day = vigorous_time_per_day * vigorous_days_per_week

            match vigorous_time_per_day:
                case num if num <= 90:
                    vigorous_time_per_day = 1
                case num if 91 <= num <= 105:
                    vigorous_time_per_day = 2
                case num if 106 <= num <= 120:
                    vigorous_time_per_day = 3
                case num if 121 <= num <= 135:
                    vigorous_time_per_day = 4
                case num if num >= 136:
                    vigorous_time_per_day = 5
                case _:
                    raise ValueError(f"UNREACHABLE: vigorous_time_per_day: {vigorous_time_per_day}")
        else:
            vigorous_time_per_day = 3
    else:
        vigorous_time_per_day = 1

    vigorous_activity_level = vigorous_time_per_day
    user_profile["vigorous_activity"] = vigorous_activity_level
    # endregion vigorous activity
    # region moderate activity
    if "moderate_days_per_week" in user_profile:
        moderate_days_per_week = user_profile["moderate_days_per_week"]
        moderate_time_per_day = user_profile["moderate_time_per_day"]
        if moderate_time_per_day is list:
            moderate_time_per_day, time_unit = moderate_time_per_day
            if time_unit == "hour":
                moderate_time_per_day = moderate_time_per_day * 60

            moderate_time_per_day = moderate_time_per_day * moderate_days_per_week

            match moderate_time_per_day:
                case num if num <= 180:
                    moderate_time_per_day = 1
                case num if 181 <= num <= 210:
                    moderate_time_per_day = 2
                case num if 211 <= num <= 240:
                    moderate_time_per_day = 3
                case num if 241 <= num <= 270:
                    moderate_time_per_day = 4
                case num if num >= 271:
                    moderate_time_per_day = 5
                case _:
                    raise ValueError(f"UNREACHABLE: moderate_time_per_day: {moderate_time_per_day}")
        else:
            moderate_time_per_day = 3
    else:
        moderate_time_per_day = 1

    moderate_activity_level = moderate_time_per_day
    user_profile["moderate_activity"] = moderate_activity_level
    # endregion moderate activity
    # region walking
    # https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/walking/art-20046261#:~:text=You%20might%20start%20with%20five,most%20days%20of%20the%20week.
    if "walking_days_per_week" in user_profile:
        walking_days_per_week = user_profile["walking_days_per_week"]
        walking_time_per_day = user_profile["walking_time_per_day"]
        if walking_time_per_day is list:
            walking_time_per_day, time_unit = walking_time_per_day
            if time_unit == "hour":
                walking_time_per_day = walking_time_per_day * 60

            walking_time_per_day = walking_time_per_day * walking_days_per_week

            # min 210 minutes per week
            # max 420 minutes per week
            match walking_time_per_day:
                case num if num <= 252:
                    walking_time_per_day = 1
                case num if 253 <= num <= 294:
                    walking_time_per_day = 2
                case num if 296 <= num <= 336:
                    walking_time_per_day = 3
                case num if 337 <= num <= 378:
                    walking_time_per_day = 4
                case num if num >= 379:
                    walking_time_per_day = 5
                case _:
                    raise ValueError(f"UNREACHABLE: walking_time_per_day: {walking_time_per_day}")
        else:
            walking_time_per_day = 3
    else:
        walking_time_per_day = 1

    walking_level = walking_time_per_day
    user_profile["walking"] = walking_level
    # endregion walking
    # region sitting
    # https://csepguidelines.ca/#:~:text=Do%20you%20know%20how%20much,periods%20of%20sitting%20where%20possible.
    sitting_time_per_day = user_profile["sitting_time_per_day"]
    if sitting_time_per_day is list:
        sitting_time_per_day, time_unit = sitting_time_per_day
        if time_unit == "hour":
            sitting_time_per_day = sitting_time_per_day * 60

        # min 0 minutes per day
        # max 8 hours per day
        match sitting_time_per_day:
            case num if num <= 96:
                sitting_time_per_day = 5
            case num if 97 <= num <= 192:
                sitting_time_per_day = 4
            case num if 193 <= num <= 288:
                sitting_time_per_day = 3
            case num if 289 <= num <= 384:
                sitting_time_per_day = 2
            case num if num >= 385:
                sitting_time_per_day = 1
    else:
        sitting_time_per_day = 3
    sitting_level = sitting_time_per_day
    user_profile["sitting"] = sitting_level
    # endregion sitting
    physical_activity_score = round(
        np.mean([vigorous_activity_level, moderate_activity_level, walking_level, sitting_level]))
    user_profile["physical_activity_level"] = physical_activity_score
    # endregion Physical activity level
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