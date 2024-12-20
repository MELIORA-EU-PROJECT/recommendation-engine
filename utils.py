import math

import json5
import numpy as np

from enum import Enum


class Objective(Enum):
    INCREASE_PHYSICAL_ACTIVITY = "increase_physical_activity"
    REDUCE_ALCOHOL_CONSUMPTION = "reduce_alcohol_consumption"
    CEASE_SMOKING = "cease_smoking"
    IMPROVE_DIET_QUALITY = "improve_diet_quality"
    IMPROVE_MENTAL_HEALTH = "improve_mental_health"
    SEEK_MEDICAL_HELP = "seek_medical_help"


# @formatter:off
# TODO: Add more items
intervention_library = {"Twitter_Post_About_Quiting_Smoking": {"goals": [Objective.CEASE_SMOKING], "ttm_stages": [1,2,3], "opr": "max"},
                        "Youtube_Video_About_Quiting_Smoking": {"goals": [Objective.CEASE_SMOKING], "ttm_stages": [2,3], "opr": "max"},
                        "News_Article_About_Diet_And_Exercise": {"goals": [Objective.IMPROVE_DIET_QUALITY,Objective.INCREASE_PHYSICAL_ACTIVITY], "ttm_stages": [2, 3], "opr": "min"},
                        "Instagram_Reel_About_Reducing_Alcohol_Intake": {"goals": [Objective.REDUCE_ALCOHOL_CONSUMPTION], "ttm_stages": [2,3,4], "opr": "max"},
                        "TikTok_About_Reducing_Alcohol_Intake": {"goals": [Objective.REDUCE_ALCOHOL_CONSUMPTION], "ttm_stages": [5], "opr": "max"},
                        "Youtube_Short_About_Quiting_Smoking": {"goals": [Objective.CEASE_SMOKING], "ttm_stages": [1,2], "opr": "max"},
                        "Youtube_Video_About_Improving_Life_Quality": {"goals": [Objective.CEASE_SMOKING,Objective.REDUCE_ALCOHOL_CONSUMPTION,Objective.IMPROVE_DIET_QUALITY,Objective.INCREASE_PHYSICAL_ACTIVITY,Objective.IMPROVE_MENTAL_HEALTH], "ttm_stages": [1,2,3], "opr": "min"},
                        "9 Proven Benefits of Physical Activity": {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY], "ttm_stages": [1,2,3], "opr": "min"},
                        "Do I need to walk 10,000 steps per day?": {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY], "ttm_stages": [1], "opr": "min"},
                        "Staying active to lower your risk of breast cancer: A simple guide to WHO’s physical activity recommendations" : {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY,Objective.IMPROVE_MENTAL_HEALTH], "ttm_stages": [4,5], "opr": "min"},
                        "Staying active to lower your risk of breast cancer: A simple guide to greek physical activity recommendations" : {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY,Objective.IMPROVE_MENTAL_HEALTH], "ttm_stages": [4,5], "opr": "min"},
                        "Staying active with breast cancer: Simple tips to keep you moving" : {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY], "ttm_stages": [5], "opr": "min"},
                        "Tips for a more active lifestyle" : {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY,Objective.IMPROVE_MENTAL_HEALTH], "ttm_stages": [1,2,3], "opr": "min"},
                        "What are the different types of physical activity?" : {"goals": [Objective.INCREASE_PHYSICAL_ACTIVITY], "ttm_stages": [1], "opr": "min"},
                        "Tobacco": {"goals": [Objective.CEASE_SMOKING], "ttm_stages": [1,2,3], "opr": "max", "ref":"https://www.who.int/news-room/fact-sheets/detail/tobacco"},
                        "Quitting tobacco": {"goals": [Objective.CEASE_SMOKING], "ttm_stages": [4,5], "opr": "max","ref":"https://www.who.int/activities/quitting-tobacco"},
                        "Smoking is the leading cause of chronic obstructive pulmonary disease": {"goals": [Objective.CEASE_SMOKING], "ttm_stages": [2,3,4,5], "opr": "max", "ref":"https://www.who.int/news/item/15-11-2023-smoking-is-the-leading-cause-of-chronic-obstructive-pulmonary-disease"},
                        "No level of alcohol consumption is safe for our health": {"goals": [Objective.REDUCE_ALCOHOL_CONSUMPTION], "ttm_stages": [1,2,3,4,5], "opr": "max", "ref":"https://www.who.int/europe/news/item/04-01-2023-no-level-of-alcohol-consumption-is-safe-for-our-health"},
                        "5 tips for a healthy diet this New Year" : {"goals": [Objective.IMPROVE_DIET_QUALITY,Objective.REDUCE_ALCOHOL_CONSUMPTION], "ttm_stages": [1,2,3], "opr": "min","ref":"https://www.who.int/news-room/feature-stories/detail/5-tips-for-a-healthy-diet-this-new-year"},
                        "Healthy diet": {"goals": [Objective.IMPROVE_DIET_QUALITY], "ttm_stages": [1,2,3,4,5], "opr": "min","ref":"https://www.who.int/news-room/fact-sheets/detail/healthy-diet"},
                        "Promoting healthy diets": {"goals": [Objective.IMPROVE_DIET_QUALITY], "ttm_stages": [3,4,5], "opr": "min","ref":"https://www.who.int/westernpacific/activities/promoting-healthy-diets"},
                        "Mental disorders": {"goals": [Objective.IMPROVE_MENTAL_HEALTH], "ttm_stages": [1,2,3,4,5], "opr": "min","ref":"https://www.who.int/news-room/fact-sheets/detail/mental-disorders"},
                        "World Mental Health Report": {"goals": [Objective.IMPROVE_MENTAL_HEALTH], "ttm_stages": [3,4,5], "opr": "min","ref":"https://www.who.int/teams/mental-health-and-substance-use/world-mental-health-report"},
                        "Determinants of health": {"goals": [Objective.SEEK_MEDICAL_HELP], "ttm_stages": [1,2,3,4,5], "opr": "min","ref":"https://www.who.int/news-room/questions-and-answers/item/determinants-of-health"},
                        }
# @formatter:on


def infer_integrated_data_layer(user_profile: dict) -> dict:
    # region General Health
    general_health = user_profile["general_health"] + 1
    user_profile["general_health"] = general_health
    # endregion General Health
    # region User Status
    if "treatment_status" in user_profile:
        treatment_status = user_profile["treatment_status"]
        match treatment_status:
            case "no, completed":
                treatment_status = "survivor"
            case "yes":
                treatment_status = "patient"
            case "no, waiting":
                treatment_status = "patient"
            case _:
                raise ValueError(f"treatment_status should be one of the following: "
                                 f"no, completed, yes, no, waiting. "
                                 f"On {user_profile} got {treatment_status}")
        user_profile["user_status"] = treatment_status
    # endregion User Status
    # region Mental Health
    mental_condition = user_profile["mental_condition"]
    if mental_condition:
        if "mental_conditions" not in user_profile:
            raise ValueError(
                f"mental_conditions should be in user_profile because 'mental_condition' flag is set. Got {user_profile}")
        mental_conditions = user_profile["mental_conditions"]
        match len(mental_conditions):
            case num if num <= 1:
                mental_condition = 5
            case num if 2 <= num <= 3:
                mental_condition = 4
            case num if 4 <= num <= 5:
                mental_condition = 3
            case num if 6 <= num <= 7:
                mental_condition = 2
            case num if num >= 8:
                mental_condition = 1
            case _:
                raise ValueError(f"UNREACHABLE: mental_conditions: {mental_conditions}")
    else:
        mental_condition = 5

    extra_perceived_problems = [
        user_profile["nervousness"],
        user_profile["worryness"],
        user_profile["depression"],
        user_profile["uninterest"],
    ]

    extra_perceived_problems = round(np.mean(extra_perceived_problems))
    match extra_perceived_problems:
        case 0:
            extra_perceived_problems = 5
        case 1:
            extra_perceived_problems = 4
        case 2:
            extra_perceived_problems = 2
        case 3:
            extra_perceived_problems = 1

    user_profile["mental_health"] = round(np.mean([mental_condition, extra_perceived_problems]))
    # endregion Mental Health
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

    if user_profile["ever_smoked"] == "never":
        duration_of_smoking = 5
    else:
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
    # region Proximity to exercise facilities
    distances_to_facilities = [
        user_profile["park_distance"],
        user_profile["open_gym_distance"],
        user_profile["gym_distance"],
        user_profile["pool_distance"],
    ]
    for i, distance in enumerate(distances_to_facilities):
        match distance:
            case "< 10 min":
                distances_to_facilities[i] = 5
            case "10-30 min":
                distances_to_facilities[i] = 3
            case "> 30 min":
                distances_to_facilities[i] = 1
            case _:
                raise ValueError(f"distance should be one of the following: "
                                 f"< 10 min, 10-30 min, > 30 min. "
                                 f"On {user_profile} got {distance}")

    user_profile["proximity_to_exercise_facilities"] = round(np.mean(distances_to_facilities))
    # endregion Proximity to exercise facilities
    # region Limitation to increase physical activity
    limiting_factors = [user_profile["lack_of_time_for_physical_activity"],
                        user_profile["lack_of_motivation_short_term"],
                        user_profile["lack_of_motivation_long_term"],
                        user_profile["feel_fatigue"],
                        user_profile["sedentary_lifestyle"],
                        user_profile["lack_of_support_from_healthcare_professionals"],
                        user_profile["lack_of_exercising_skills"],
                        user_profile["lack_of_physical_fitness"],
                        user_profile["concern_physical_condition"],
                        user_profile["lack_of_support_from_family_physical_activity"],
                        user_profile["lack_of_physical_activity_preventing_disease"],
                        user_profile["lack_of_infrastructure"],
                        user_profile["delusion"],
                        user_profile["lack_of_knowledge_on_physical_activity_recommendations"],
                        user_profile["fear_of_injury"],
                        user_profile["stigma"],
                        user_profile["weather_conditions"],
                        user_profile["safety_concerns"],
                        user_profile["uncomfortability"],
                        user_profile["accuracy_of_physical_activity_information"]]
    user_profile["limitation_to_increase_physical_activity"] = 5 - round(np.mean(limiting_factors))
    # endregion Limitation to increase physical activity
    # region Enhancing factors to increase physical activity
    enhancing_factors = [user_profile["support_from_family_physical_activity"],
                         user_profile["healthcare_professional_support_physical_activity"],
                         user_profile["knowledge_on_physical_activity_recommendations"],
                         user_profile["accessibility_of_physical_activity_infrastructure"],
                         user_profile["development_of_routine_physical_activity"],
                         user_profile["wake_up_call_physical_activity"],
                         user_profile["role_model_physical_activity"],
                         user_profile["improvement_of_energy_physical_activity"],
                         user_profile["healthcare_professional_tailored_plan"]]
    user_profile["enhancing_factors_to_increase_physical_activity"] = round(np.mean(enhancing_factors))
    # endregion Enhancing factors to increase physical activity
    # region Limitation to improve diet quality
    limiting_factors = [user_profile["cost_of_healthy_food"],
                        user_profile["high_availability_of_fast_food"],
                        user_profile["lack_of_good_quality_food"],
                        user_profile["lack_of_time"],
                        user_profile["lack_of_support_from_family"],
                        user_profile["difficulty_in_avoiding_unhealthy_food_on_social_occasions"],
                        user_profile["unhealthy_family_eating_habits"],
                        user_profile["lack_of_support_from_healthcare_system"],
                        user_profile["lack_of_knowledge_toward_healthier_life"],
                        user_profile["lack_of_knowledge_on_current_healthy_eating_recommendations"],
                        user_profile["lack_of_knowledge_on_healthy_food_preparation"],
                        user_profile["accuracy_of_healthy_eating_information"],
                        user_profile["lack_of_effort"],
                        user_profile["temptation_resistance"],
                        user_profile["craving"],
                        user_profile["dislike_of_healthy_food_taste"],
                        user_profile["lack_of_motivation"],
                        user_profile["lack_of_healthy_food_preventing_disease"]]

    user_profile["limitation_to_improve_diet_quality"] = 5 - round(np.mean(limiting_factors))
    # endregion Limitation to improve diet quality
    # region Enhancing factors to improve diet quality
    enhancing_factors = [user_profile["low_cost_of_healthy_food"],
                         user_profile["accessibility_of_good_quality_food"],
                         user_profile["reduction_to_costs_of_healthy_food"],
                         user_profile["help_in_food_preparation"],
                         user_profile["support_from_family"],
                         user_profile["healthcare_professional_support"],
                         user_profile["support_of_knowledge_on_healthy_eating_recommendations"],
                         user_profile["accountability_partner"],
                         user_profile["collaboration_with_healthcare_professionals"],
                         user_profile["skills_on_healthy_food_preparation"],
                         user_profile["wake_up_call"],
                         user_profile["development_of_routine"],
                         user_profile["improvement_of_energy"],
                         user_profile["role_model"]]
    user_profile["enhancing_factors_to_improve_diet_quality"] = round(np.mean(enhancing_factors))
    # endregion Enhancing factors to improve diet quality
    # region Level of symptoms
    symptoms = [user_profile["pain"],
                user_profile["fatigue"],
                user_profile["nausea"],
                user_profile["constipation"],
                user_profile["disturbed_sleep"],
                user_profile["shortness_of_breath"],
                user_profile["lack_of_appetite"],
                user_profile["drowsiness"],
                user_profile["dry_mouth"],
                ]

    # https://stackoverflow.com/a/51494556/13250408
    user_profile["level_of_symptoms"] = round((5 - 0) * (np.mean(symptoms) - 0) / (10 - 0) + 0)
    # endregion Level of symptoms
    # region Quality of life
    qol = user_profile["quality_of_life"] + 1
    user_profile["quality_of_life"] = qol
    # endregion Quality of life
    return user_profile


def infer_aggregated_data_layer(user_profile: dict) -> dict:
    return_dict = {}
    # region increase physical activity
    xs = [user_profile["physical_activity_level"], user_profile["limitation_to_increase_physical_activity"],
          user_profile["enhancing_factors_to_increase_physical_activity"],
          user_profile["proximity_to_exercise_facilities"], user_profile["general_health"]]
    xs = [min_max_transform(x, 1, 5) for x in xs]
    ws = [8, 6, 6, 4, 3]
    assert len(xs) == len(xs) == len(
        ws), f"xs, xs and ws should have the same length. got xs: {len(xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["increase_physical_activity"] = v
    # endregion increase physical activity
    # region improve diet quality
    xs = [user_profile["eating_pyramid_score"], user_profile["limitation_to_improve_diet_quality"],
          user_profile["enhancing_factors_to_improve_diet_quality"], user_profile["general_health"]]
    xs = [min_max_transform(x, 1, 5) for x in xs]
    ws = [8, 5, 5, 3]
    assert len(xs) == len(xs) == len(
        ws), f"xs, xs and ws should have the same length. got xs: {len(xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["improve_diet_quality"] = v
    # endregion improve diet quality
    # region reduce alcohol consumption
    xs = [user_profile["alcohol_consumption"], user_profile["general_health"]]
    xs = [min_max_transform(x, 1, 5) for x in xs]
    ws = [10, 4]
    assert len(xs) == len(xs) == len(
        ws), f"xs, xs and ws should have the same length. got xs: {len(xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["reduce_alcohol_consumption"] = v
    # endregion reduce alcohol consumption
    # region cease smoking
    xs = [user_profile["usage_of_tobacco_products"], user_profile["general_health"]]
    xs = [min_max_transform(x, 1, 5) for x in xs]
    ws = [10, 3]
    assert len(xs) == len(xs) == len(
        ws), f"xs, xs and ws should have the same length. got xs: {len(xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["cease_smoking"] = v
    # endregion cease smoking
    # region improve mental health
    xs = [user_profile["mental_health"], user_profile["quality_of_life"], user_profile["general_health"]]
    xs = [min_max_transform(x, 1, 5) for x in xs]
    ws = [10, 6, 4]
    assert len(xs) == len(xs) == len(
        ws), f"xs, xs and ws should have the same length. got xs: {len(xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["improve_mental_health"] = v
    # endregion
    # region seek medical help
    xs = [user_profile["level_of_symptoms"], user_profile["mental_health"], user_profile["general_health"],
          user_profile["physical_activity_level"], user_profile["quality_of_life"]]
    xs = [min_max_transform(x, 1, 5) for x in xs]
    ws = [10, 6, 9, 2, 5]
    assert len(xs) == len(xs) == len(
        ws), f"xs, xs and ws should have the same length. got xs: {len(xs)}, xs: {len(xs)}, ws: {len(ws)}"
    v_prime = normalized_manhattan_distance(xs, ws)
    v = map_v_prime_to_v(v_prime)
    return_dict["seek_medical_help"] = v
    # endregion

    return return_dict


def add_ttm_stages(user_profile: dict) -> dict:
    return_dict = {}
    # region "increase_physical_activity"
    return_dict[Objective.INCREASE_PHYSICAL_ACTIVITY.value] = {"str": user_profile["increase_physical_activity"],
                                                               "ttm_stages": 4}
    # endregion
    # region "improve_diet_quality"
    return_dict[Objective.IMPROVE_DIET_QUALITY.value] = {"str": user_profile["improve_diet_quality"], "ttm_stages": 4}
    # endregion
    # region "reduce_alcohol_consumption"
    return_dict[Objective.REDUCE_ALCOHOL_CONSUMPTION.value] = {"str": user_profile["reduce_alcohol_consumption"],
                                                               "ttm_stages": 4}
    # endregion
    # region "cease_smoking"
    return_dict[Objective.CEASE_SMOKING.value] = {"str": user_profile["cease_smoking"], "ttm_stages": 4}
    # endregion
    # region "improve_mental_health"
    return_dict[Objective.IMPROVE_MENTAL_HEALTH.value] = {"str": user_profile["improve_mental_health"], "ttm_stages": 4}
    # endregion
    # region "seek_medical_help"
    return_dict[Objective.SEEK_MEDICAL_HELP.value] = {"str": user_profile["seek_medical_help"], "ttm_stages": 4}
    # endregion
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
        for behavior in intervention_properties["goals"]:
            behavior = behavior.value
            if behavior in user_profile:
                distances.append(abs(user_profile[behavior]["str"] - 1))

        if len(distances) == 0:
            raise ValueError(
                f"There seems to be a mismatch of behaviours between the user profile and the intervention library.\n"
                f"Intervention: {intervention_title}, Behaviours: {intervention_properties['goals']}\n"
                f"User profile: {user_profile}\n"
                f"Make sure that the behaviours in the intervention library are present in the user profile.")
        if intervention_operator == "min":
            sim = 1 - np.min(distances)
        elif intervention_operator == "max":
            sim = 1 - np.max(distances)
        elif intervention_operator == "weighted":
            raise NotImplementedError("Weighted operator is not implemented yet.")

        sim_need_dict[intervention_title] = {"sim_need": sim, "goals": intervention_properties["goals"]}

    return sim_need_dict


def sim_stage(user_profile: dict, intervention_library: dict):
    sim_stage_dict = {}
    for intervention_title, intervention_properties in intervention_library.items():
        relevant_behaviors_stages = []
        for behavior in intervention_properties["goals"]:
            behavior = behavior.value
            if behavior in user_profile:
                relevant_behaviors_stages.append(user_profile[behavior]["ttm_stages"])

        for stage in intervention_properties["ttm_stages"]:
            if stage in relevant_behaviors_stages:
                sim_stage_dict[intervention_title] = 1.0

        min_distance = math.inf
        if intervention_title not in sim_stage_dict:
            for i in relevant_behaviors_stages:
                for j in intervention_properties["ttm_stages"]:
                    if abs(i - j) < min_distance:
                        min_distance = abs(i - j)
            sim_stage_dict[intervention_title] = 1 - 0.25 * min_distance

    return sim_stage_dict


def sim_total(sim_needs, sim_stages):
    sim_total_dict = {}
    for intervention_title in sim_needs:
        if sim_needs[intervention_title]["sim_need"] >= 0.5:
            sim_total_dict[intervention_title] = {
                "sim_total": 0.5 * sim_needs[intervention_title]["sim_need"] + 0.5 * sim_stages[
                    intervention_title], "goals": sim_needs[intervention_title]["goals"]}
        else:
            sim_total_dict[intervention_title] = {"sim_total": 0, "goals": sim_needs[intervention_title]["goals"]}

    return sim_total_dict


def diff_user_profile(new_user_profile: dict, old_user_profile: dict) -> dict:
    return_dict = {}
    for new_key, new_value in new_user_profile.items():
        if new_key in old_user_profile:
            if new_value != old_user_profile[new_key]:
                return_dict[new_key] = new_value
        else:
            return_dict[new_key] = new_value

    return return_dict


def get_recommendations(user_profile):
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
    ttm_user_profile = {k: {"str": min_max_transform(v["str"], 1, 5), "ttm_stages": v["ttm_stages"]}
                        for k, v in ttm_user_profile.items()}
    sim_needs = sim_need(ttm_user_profile, intervention_library)
    sim_stages = sim_stage(ttm_user_profile, intervention_library)
    sim_totals = sim_total(sim_needs, sim_stages)
    sim_totals_filtered = {k: v for k, v in sim_totals.items() if v["sim_total"] >= 0.5}
    sim_total_ordered = dict(sorted(sim_totals_filtered.items(), key=lambda x: x[1]["sim_total"], reverse=True))
    for item_title, item_properties in sim_total_ordered.items():
        sim_total_ordered[item_title]["goals"] = [g.value for g in item_properties["goals"]]
    results = {"recommendations": sim_total_ordered, "user_profile": ttm_user_profile,
               "diffs": {"integrated": integrated_layer_profile, "aggregated": agregated_layer_profile,
                         "ttm": ttm_layer_profile}}
    print(f"Recommendations: {json5.dumps(results, indent=4, quote_keys=True)}")
    return results


def filter_recommendations(recommendations: dict, objective: str):
    return_dict = {}
    for intervention_title, intervention_properties in recommendations.items():
        if objective in intervention_properties["goals"]:
            return_dict[intervention_title] = intervention_properties
    return return_dict