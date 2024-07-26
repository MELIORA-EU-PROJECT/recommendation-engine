import numpy as np


def infer_integrated_data_layer(user_profile: dict) -> dict:
    # region Recovery during sleep
    recovery_during_sleep = np.mean(user_profile["recovery_during_sleep_vector"])
    if recovery_during_sleep <= 24:
        recovery_during_sleep = 1
    elif recovery_during_sleep <= 49:
        recovery_during_sleep = 2
    elif recovery_during_sleep <= 74:
        recovery_during_sleep = 3
    elif recovery_during_sleep <= 100:
        recovery_during_sleep = 5
    else:
        raise ValueError(
            f"Recovery during sleep should be between 0 and 100. Got {recovery_during_sleep} on {user_profile}")

    max_missing_heartrate_percentage = np.max(user_profile["missing_heart_rate_percentage_vector"])

    if max_missing_heartrate_percentage < 20:
        confidence = 0.01 * (100 - max_missing_heartrate_percentage)
    elif max_missing_heartrate_percentage < 80:
        confidence = 0.01 * (80 - max_missing_heartrate_percentage)
    elif max_missing_heartrate_percentage <= 100:
        confidence = 0
    else:
        raise ValueError(
            f"Max missing heart rate percentage should be between 0 and 100. Got {max_missing_heartrate_percentage} on {user_profile}")

    user_profile["recovery_during_sleep"] = [recovery_during_sleep, confidence]
    # endregion Recovery during sleep
    # region Recovery during 24-Hours
    recovery_during_24_hours = np.mean(user_profile["recovery_during_day_vector"])
    if recovery_during_24_hours <= 9:
        recovery_during_24_hours = 1
    elif recovery_during_24_hours <= 19:
        recovery_during_24_hours = 2
    elif recovery_during_24_hours <= 29:
        recovery_during_24_hours = 3
    elif recovery_during_24_hours <= 30:
        recovery_during_24_hours = 5
    else:
        raise ValueError(
            f"Recovery during 24 hours should be between 0 and 30. Got {recovery_during_24_hours} on {user_profile}")

    if max_missing_heartrate_percentage < 20:
        confidence = 0.01 * (100 - max_missing_heartrate_percentage)
    elif max_missing_heartrate_percentage < 80:
        confidence = 0.01 * (80 - max_missing_heartrate_percentage)
    elif max_missing_heartrate_percentage <= 100:
        confidence = 0
    else:
        raise ValueError(
            f"Max missing heart rate percentage should be between 0 and 100. Got {max_missing_heartrate_percentage} on {user_profile}")

    user_profile["recovery_during_24_hours"] = [recovery_during_24_hours, confidence]
    # endregion Recovery during 24-Hours
    # region Perceived Sleep Problems
    perceived_sleep_problems = user_profile["perceived_sleep_problems"]
    user_profile["perceived_sleep_problems"] = [perceived_sleep_problems, 0.8]
    # endregion Perceived Sleep Problems
    # region Perceived sleep sufficiency
    perceived_sleep_sufficiency = user_profile["perceived_sleep_sufficiency"]
    user_profile["perceived_sleep_sufficiency"] = [perceived_sleep_sufficiency, 0.8]
    # endregion Perceived sleep sufficiency
    # region Sleep quality
    perceived_sleep_problems, _ = user_profile["perceived_sleep_problems"]
    recovery_during_sleep, recovery_during_sleep_confidence = user_profile["recovery_during_sleep"]
    if recovery_during_sleep_confidence <= 0.6:
        sleep_quality = perceived_sleep_problems
        confidence = 0.8
    else:
        sleep_quality = min(perceived_sleep_problems, recovery_during_sleep)
        x_prime = min_max_transform(recovery_during_sleep, 1, 5)
        y_prime = min_max_transform(perceived_sleep_problems, 1, 5)
        confidence = 1 - abs(x_prime - y_prime)

    user_profile["sleep_quality"] = [sleep_quality, confidence]
    # endregion Sleep quality
    # region Perceived stress
    perceived_stress = user_profile["perceived_stress"]
    user_profile["perceived_stress"] = [perceived_stress, 0.8]
    # endregion Perceived stress
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
    # region Perceived physical activity level
    perceived_physical_activity_level = user_profile["perceived_physical_activity"]
    user_profile["perceived_physical_activity_level"] = [perceived_physical_activity_level, 0.8]
    # endregion Perceived physical activity level
    # region Physical activity level
    physical_activity_level = np.sum(user_profile["physical_activity_points_vector"])
    if physical_activity_level <= 29:
        physical_activity_level = 1
    elif physical_activity_level <= 59:
        physical_activity_level = 2
    elif physical_activity_level <= 94:
        physical_activity_level = 3
    elif physical_activity_level <= 129:
        physical_activity_level = 4
    elif physical_activity_level <= 300:
        physical_activity_level = 5
    else:
        raise ValueError(
            f"Physical activity level should be between 0 and 300. Got {physical_activity_level} on {user_profile}")

    if max_missing_heartrate_percentage < 20:
        confidence = 0.01 * (100 - max_missing_heartrate_percentage)
    elif max_missing_heartrate_percentage < 80:
        confidence = 0.01 * (80 - max_missing_heartrate_percentage)
    elif max_missing_heartrate_percentage <= 100:
        confidence = 0
    else:
        raise ValueError(
            f"Max missing heart rate percentage should be between 0 and 100. Got {max_missing_heartrate_percentage} on {user_profile}")

    user_profile["physical_activity_level"] = [physical_activity_level, confidence]

    # endregion Physical activity level
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
    # region Vegetable Fruit Intake
    vegetable_fruit_consumption = user_profile["vegetables_fruits"]
    user_profile["vegetable_fruit_consumption"] = [vegetable_fruit_consumption, 0.8]
    # endregion Vegetable Fruit Intake
    # region Excessive intake of unhealthy foods
    excessive_intake_of_unhealthy_foods = user_profile["fast_food"]
    user_profile["excessive_intake_of_unhealthy_foods"] = [excessive_intake_of_unhealthy_foods, 0.8]
    # endregion Excessive intake of unhealthy foods
    # region Eating Rhythm
    eating_rhythm = user_profile["eating_rhythm"]
    user_profile["eating_rhythm"] = [eating_rhythm, 0.8]
    # endregion Eating Rhythm
    # region Emotional eating
    emotional_eating = user_profile["emotional_eating"]
    user_profile["emotional_eating"] = [emotional_eating, 0.8]
    # endregion Emotional eating
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
    return user_profile


def infer_aggregated_data_layer(user_profile: dict) -> dict:
    raise NotImplementedError("This function is not implemented yet.")


def min_max_transform(x, x_min, x_max):
    return (x - x_min) / (x_max - x_min)