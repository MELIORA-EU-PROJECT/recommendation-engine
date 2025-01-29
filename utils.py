import math
import os

import json5
import numpy as np

from enum import Enum

import requests
from colorama import Fore, Style


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
mini_course_physical_activity = {
	"mini_course_id": "123",
	"title": "Physical Activity Mini Course",
	"objectives": [Objective.INCREASE_PHYSICAL_ACTIVITY],
	"goals": [{
		"description": "Increase the daily number of steps",
		"day": 4,
		"category": "physical_activity",
		# "indicator":,
		"target": {
			"goal": 10000,
			"units": "steps per day",
			"condition": "gte"
		},
		"motivational_tips": [
			{
				"stage": "Fully achieved",
				"tip_text": "Congratulations! You have achieved your goal. Walking more next week will be even better!",
				"tip_videos": None
			},
			{
				"stage": "Partially achieved",
				"tip_text": "You are doing great! Keep it up!",
				"tip_videos": None
			},
			{
				"stage": "Not achieved at all",
				"tip_text": "It's never too late to start walking more. Start with small steps and increase gradually.",
				"tip_videos": None
			}
		]

	}],
	"educational_materials": [
		{1: ["Not Implemented Yet"],
		 2: ["Not Implemented Yet"],
		 3: ["Not Implemented Yet"],
		 4: ["64d29f7e92cb40a5c4567d12"],
		 5: ["Not Implemented Yet"],
		 6: ["Not Implemented Yet"],
		 7: ["Not Implemented Yet"],
		 },
	],
	"language": "Greek",
	"end_of_week_mini_quiz": {
		"day": 7,
		"questions": [
			{
				"question": "What is the recommended daily number of steps?",
				"possible_answers": [
					"5000",
					"10000",
					"15000"
				],
				"correct_answer": [1]
			},
			{
				"question": "How many minutes of moderate physical activity are recommended per week?",
				"possible_answers": [
					"150",
					"450"
					"300",
				],
				"correct_answer": [2]
			}
		]
	},
	"default_schedule": [
		{
			"day": 1,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				}
			]
		},
		{
			"day": 2,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				}
			]
		}, {
			"day": 3,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				}
			]
		}, {
			"day": 4,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				}
			]
		}, {
			"day": 5,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				}
			]
		}, {
			"day": 6,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				}
			]
		}, {
			"day": 7,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
				{
					"time": "12:00",
					"type": "educational_material"
				},
				{
					"time": "18:00",
					"type": "end_of_week_mini_quiz"
				}
			]
		}, {
			"day": 8,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
			]
		}, {
			"day": 9,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
			]
		}, {
			"day": 10,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
			]
		}, {
			"day": 11,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
			]
		}, {
			"day": 12,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
			]
		}, {
			"day": 13,
			"order": [
				{
					"time": "08:00",
					"type": "goal"
				},
			]
		}, {
			"day": 14,
			"order": [
				{
					"time": "12:00",
					"type": "end_of_week_mini_quiz"
				}
			]
		},
	]
}
mini_course_library = {mini_course_physical_activity["mini_course_id"]: mini_course_physical_activity}


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

	three_or_more_red_meat_weekly = user_profile["three_or_more_red_meat_weekly"]
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

	aggregate_distances = three_or_more_red_meat_weekly + how_often_fruit + how_often_vegetables + how_often_nuts + how_often_fish + how_often_whole_grain + how_often_refined_grain + how_often_low_fat_dairy + how_often_high_fat_dairy + how_often_sweets
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
		if isinstance(vigorous_time_per_day, list):
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
		if isinstance(moderate_time_per_day, list):
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
		if isinstance(walking_time_per_day, list):
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
	if isinstance(sitting_time_per_day, list):
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
	with open("scrap/example_patient_integrated.json", "w") as write_file:
		json5.dump(user_profile, write_file, indent=4, quote_keys=True)
	print(f"Integrated Data Layer: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	# Diff User Profile
	integrated_layer_profile = diff_user_profile(user_profile, old_user_profile)
	print(f"Diff User Profile: {json5.dumps(integrated_layer_profile, indent=4, quote_keys=True)}")
	# Aggregated Data Layer
	old_user_profile = user_profile
	user_profile = infer_aggregated_data_layer(user_profile)
	with open("scrap/example_patient_aggregated.json", "w") as write_file:
		json5.dump(user_profile, write_file, indent=4, quote_keys=True)
	print(f"Aggregated Data Layer: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	# Diff User Profile
	agregated_layer_profile = diff_user_profile(user_profile, old_user_profile)
	print(f"Diff User Profile: {json5.dumps(agregated_layer_profile, indent=4, quote_keys=True)}")
	# TTM stages
	old_user_profile = user_profile
	ttm_user_profile = add_ttm_stages(user_profile)
	with open("scrap/example_patient_ttm.json", "w") as write_file:
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
	recommendations = [{"title": k, "info": v} for k, v in sim_total_ordered.items()]
	results = {"recommendations": recommendations, "user_profile": ttm_user_profile,
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


def get_day_by_user_id(user_id: int):
	return {"day": 4}


def create_user_profile(userId: str):
	url = f"https://datacollection.risa.eu/onboarding/participantsBaseline/{userId}"
	url_ids = "https://datacollection.risa.eu/onboarding/onboardingQuestionnaire/ids"

	headers = {
		"Authorization": os.getenv("BASIC_AUTHORIZATION_ONBOARDING_QUESTIONNAIRE")
	}

	response = requests.get(url_ids, headers=headers)
	question_ids = response.json()
	print(f"IDs: {question_ids}")

	temp_user_profile = {}
	for question_id in question_ids:
		response = requests.get(f"{url}/{question_id}", headers=headers)
		if response.status_code != 200:
			print(f"Question: {question_id}, {Fore.YELLOW}{response.status_code}{Style.RESET_ALL}")
		else:
			print(f"Question: {question_id}, {Fore.GREEN}{response.status_code}{Style.RESET_ALL}")

		try:
			print(json5.dumps(response.json(), indent=4, quote_keys=True))

			# Checking if response is empty
			if isinstance(response.json(), list) and len(response.json()) == 0:
				temp_user_profile[question_id] = None
				continue

			temp_user_profile[question_id] = response.json()

		except:
			print(f"No JSON response")
			temp_user_profile[question_id] = None

	print(f"User Profile: {json5.dumps(temp_user_profile, indent=4, quote_keys=True)}")

	user_profile = {}

	if "year_of_birth" in temp_user_profile:
		if temp_user_profile["year_of_birth"] is not None:
			user_profile["year_of_birth"] = int(temp_user_profile["year_of_birth"][0]["answer"])
	if "ethnic_group" in temp_user_profile:
		if temp_user_profile["ethnic_group"] is not None:
			user_profile["ethnic_group"] = temp_user_profile["ethnic_group"][0]["answer"]
	if "origin_country" in temp_user_profile:
		if temp_user_profile["origin_country"] is not None:
			user_profile["country_of_origin"] = temp_user_profile["origin_country"][0]["answer"]
	if "current_country" in temp_user_profile:
		if temp_user_profile["current_country"] is not None:
			user_profile["current_country"] = temp_user_profile["current_country"][0]["answer"]
	if "area" in temp_user_profile:
		if temp_user_profile["area"] is not None:
			user_profile["current_living_area"] = temp_user_profile["area"][0]["answer"]
	# if "postcode" in temp_user_profile:
	#     if temp_user_profile["postcode"] is not None:
	if "marital_status" in temp_user_profile:
		if temp_user_profile["marital_status"] is not None:
			user_profile["marital_status"] = temp_user_profile["marital_status"][0]["answer"]
	if "education_level" in temp_user_profile:
		if temp_user_profile["education_level"] is not None:
			user_profile["highest_education"] = temp_user_profile["education_level"][0]["answer"]
	if "present_work" in temp_user_profile:
		if temp_user_profile["present_work"] is not None:
			user_profile["current_employment"] = temp_user_profile["present_work"][0]["answer"]
	if "household_economy" in temp_user_profile:
		if temp_user_profile["household_economy"] is not None:
			user_profile["household_economic_status"] = temp_user_profile["household_economy"][0]["answer"]
	if "caring_responsibilities" in temp_user_profile:
		if temp_user_profile["caring_responsibilities"] is not None:
			user_profile["caregiver"] = True if temp_user_profile["caring_responsibilities"][0][
													"answer"] == "yes" else False
	# if "dog_owner" in temp_user_profile:
	#     if temp_user_profile["dog_owner"] is not None:
	if "general_health" in temp_user_profile:
		if temp_user_profile["general_health"] is not None:
			temp = temp_user_profile["general_health"][0]["answer"]
			if temp == "very_good":
				user_profile["general_health"] = 4
			elif temp == "good":
				user_profile["general_health"] = 3
			elif temp == "neither_poor_or_good":
				user_profile["general_health"] = 2
			elif temp == "poor":
				user_profile["general_health"] = 1
			elif temp == "very_poor":
				user_profile["general_health"] = 0
			else:
				raise ValueError(f"Invalid general_health value: {temp}")
	if "height_on-boarding" in temp_user_profile:
		if temp_user_profile["height_on-boarding"] is not None:
			user_profile["height"] = int(temp_user_profile["height_on-boarding"][0]["answer"]) / 100
	if "weight_on-boarding" in temp_user_profile:
		if temp_user_profile["weight_on-boarding"] is not None:
			user_profile["weight"] = int(temp_user_profile["weight_on-boarding"][0]["answer"])
	if "breast_cancer_diagnosis" in temp_user_profile:
		if temp_user_profile["breast_cancer_diagnosis"] is not None:
			user_profile["diagnosis"] = True if temp_user_profile["breast_cancer_diagnosis"][0][
													"answer"] == "yes" else False
	if "breast_cancer_diagnosis_date" in temp_user_profile:
		if temp_user_profile["breast_cancer_diagnosis_date"] is not None:
			user_profile["first_diagnosis"] = temp_user_profile["breast_cancer_diagnosis_date"][0]["answer"]
	if "currently_receiving_breast_cancer_treatment" in temp_user_profile:
		if temp_user_profile["currently_receiving_breast_cancer_treatment"] is not None:
			user_profile["treatment_status"] = temp_user_profile["currently_receiving_breast_cancer_treatment"][0][
				"answer"]
	if "current_breast_cancer_treatments" in temp_user_profile:
		if temp_user_profile["current_breast_cancer_treatments"] is not None:
			temp = []
			for item in temp_user_profile["current_breast_cancer_treatments"]:
				temp.append(item["answer"])

			user_profile["treatment_type"] = temp
	if "last_breast_cancer_treatment_date" in temp_user_profile:
		if temp_user_profile["last_breast_cancer_treatment_date"] is not None:
			user_profile["last_treatment"] = temp_user_profile["last_breast_cancer_treatment_date"][0]["answer"]
	if "schedule_for_breast_cancer_treatment" in temp_user_profile:
		if temp_user_profile["schedule_for_breast_cancer_treatment"] is not None:
			user_profile["waiting_first_treatment"] = temp_user_profile["schedule_for_breast_cancer_treatment"][0][
				"answer"]
	if "current_status_breast_cancer" in temp_user_profile:
		if temp_user_profile["current_status_breast_cancer"] is not None:
			user_profile["cancer_free"] = temp_user_profile["current_status_breast_cancer"][0]["answer"]
	if "chronic_medical_condition_diagnosis" in temp_user_profile:
		if temp_user_profile["chronic_medical_condition_diagnosis"] is not None:
			user_profile["chronic_condition"] = True if temp_user_profile["chronic_medical_condition_diagnosis"][0][
															"answer"] == "yes" else False
	if "chronic_medical_conditions" in temp_user_profile:
		if temp_user_profile["chronic_medical_conditions"] is not None:
			temp = []
			for item in temp_user_profile["chronic_medical_conditions"]:
				temp.append(item["answer"])

			user_profile["chronic_conditions"] = temp
	if "mental_health_condition_diagnosis" in temp_user_profile:
		if temp_user_profile["mental_health_condition_diagnosis"] is not None:
			user_profile["mental_condition"] = True if temp_user_profile["mental_health_condition_diagnosis"][0][
														   "answer"] == "yes" else False
	if "mental_health_conditions" in temp_user_profile:
		if temp_user_profile["mental_health_conditions"] is not None:
			temp = []

			for item in temp_user_profile["mental_health_conditions"]:
				temp.append(item["answer"])

			user_profile["mental_conditions"] = temp
	if "recent_problems_frequency" in temp_user_profile:
		if temp_user_profile["recent_problems_frequency"] is not None:
			for option in temp_user_profile["recent_problems_frequency"]:

				if option["answer"] == "not_at_all":
					value = 0
				elif option["answer"] == "several_days":
					value = 1
				elif option["answer"] == "more_than_half":
					value = 2
				elif option["answer"] == "nearly_everyday":
					value = 3
				else:
					raise ValueError(f"Invalid recent_problems_frequency value: {option['answer']}")

				if option["option"] == "feeling_nervous":
					user_profile["nervousness"] = value
				elif option["option"] == "cant_control_worrying":
					user_profile["worryness"] = value
				elif option["option"] == "feeling_down":
					user_profile["depression"] = value
				elif option["option"] == "little_interest":
					user_profile["uninterest"] = value
				else:
					raise ValueError(f"Invalid recent_problems_frequency option: {option['option']}")
	if "symptoms_experienced_last_week" in temp_user_profile:
		if temp_user_profile["symptoms_experienced_last_week"] is not None:
			for option in temp_user_profile["symptoms_experienced_last_week"]:
				if option["option"] == "pain":
					user_profile["pain"] = int(option["answer"])
				elif option["option"] == "fatigue":
					user_profile["fatigue"] = int(option["answer"])
				elif option["option"] == "nausea":
					user_profile["nausea"] = int(option["answer"])
				elif option["option"] == "constipation_diarrhoea":
					user_profile["constipation"] = int(option["answer"])
				elif option["option"] == "d_sleep":
					user_profile["disturbed_sleep"] = int(option["answer"])
				elif option["option"] == "s_breath":
					user_profile["shortness_of_breath"] = int(option["answer"])
				elif option["option"] == "l_appetite":
					user_profile["lack_of_appetite"] = int(option["answer"])
				elif option["option"] == "drowsy":
					user_profile["drowsiness"] = int(option["answer"])
				elif option["option"] == "dry_mouth":
					user_profile["dry_mouth"] = int(option["answer"])
				else:
					raise ValueError(f"Invalid symptoms_experienced_last_week option: {option['option']}")
	if "quality_of_life" in temp_user_profile:
		if temp_user_profile["quality_of_life"] is not None:
			value = temp_user_profile["quality_of_life"][0]["answer"]
			if value == "very_poorpoor":
				user_profile["quality_of_life"] = 0
			elif value == "poor":
				user_profile["quality_of_life"] = 1
			elif value == "neither_poor_or_good":
				user_profile["quality_of_life"] = 2
			elif value == "good":
				user_profile["quality_of_life"] = 3
			else:
				raise ValueError(f"Invalid quality_of_life value: {value}")
	if "first_degree_breast_cancer" in temp_user_profile:
		if temp_user_profile["first_degree_breast_cancer"] is not None:
			user_profile["number_of_relatives_with_breast_cancer"] = temp_user_profile["first_degree_breast_cancer"][0][
				"answer"]
	if "has_given_birth" in temp_user_profile:
		if temp_user_profile["has_given_birth"] is not None:
			user_profile["given_birth"] = temp_user_profile["has_given_birth"][0]["answer"]
	if "current_menstrual_status" in temp_user_profile:
		if temp_user_profile["current_menstrual_status"] is not None:
			user_profile["current_menstrual_status"] = temp_user_profile["current_menstrual_status"][0]["answer"]
	if "breastfed_6_months" in temp_user_profile:
		if temp_user_profile["breastfed_6_months"] is not None:
			user_profile["breastfeeding"] = True if temp_user_profile["breastfed_6_months"][0][
														"answer"] == "yes" else False
	if "contraceptives_or_hormones" in temp_user_profile:
		if temp_user_profile["contraceptives_or_hormones"] is not None:
			user_profile["contraceptive_use"] = True if temp_user_profile["contraceptives_or_hormones"][0][
															"answer"] == "yes" else False
	if "alcohol_consumption_frequency" in temp_user_profile:
		if temp_user_profile["alcohol_consumption_frequency"] is not None:
			user_profile["how_often_alcohol"] = temp_user_profile["alcohol_consumption_frequency"][0]["answer"]
	if "typical_daily_alcohol_intake" in temp_user_profile:
		if temp_user_profile["typical_daily_alcohol_intake"] is not None:
			user_profile["drinks_per_session"] = temp_user_profile["typical_daily_alcohol_intake"][0]["answer"]
		else:
			user_profile["drinks_per_session"] = "1-2"
	if "frequent_heavy_drinking" in temp_user_profile:
		if temp_user_profile["frequent_heavy_drinking"] is not None:
			user_profile["how_often_6_or_more_drinks"] = temp_user_profile["frequent_heavy_drinking"][0]["answer"]
		else:
			user_profile["how_often_6_or_more_drinks"] = "never"
	if "eats_red_meat_weekly" in temp_user_profile:
		if temp_user_profile["eats_red_meat_weekly"] is not None:
			user_profile["three_or_more_red_meat_weekly"] = True if temp_user_profile["eats_red_meat_weekly"][0][
																		"answer"] == "yes" else False
	if "fresh_fruit_consumption" in temp_user_profile:
		if temp_user_profile["fresh_fruit_consumption"][0] is not None:
			value = ""
			if temp_user_profile["fresh_fruit_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["fresh_fruit_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["fresh_fruit_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["fresh_fruit_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["fresh_fruit_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["fresh_fruit_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_fruit"] = value
	if "vegetable_consumption" in temp_user_profile:
		if temp_user_profile["vegetable_consumption"][0] is not None:

			value = ""
			if temp_user_profile["vegetable_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["vegetable_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["vegetable_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["vegetable_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["vegetable_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["vegetable_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_vegetables"] = value
	if "legumes_nuts_seeds_consumption" in temp_user_profile:
		if temp_user_profile["legumes_nuts_seeds_consumption"][0] is not None:
			value = ""
			if temp_user_profile["legumes_nuts_seeds_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["legumes_nuts_seeds_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["legumes_nuts_seeds_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["legumes_nuts_seeds_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["legumes_nuts_seeds_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["legumes_nuts_seeds_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_nuts"] = value
	if "fish_seafood_consumption" in temp_user_profile:
		if temp_user_profile["fish_seafood_consumption"][0] is not None:
			value = ""
			if temp_user_profile["fish_seafood_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["fish_seafood_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["fish_seafood_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["fish_seafood_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["fish_seafood_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["fish_seafood_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_fish"] = value
	if "whole_grains_consumption" in temp_user_profile:
		if temp_user_profile["whole_grains_consumption"][0] is not None:

			value = ""
			if temp_user_profile["whole_grains_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["whole_grains_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["whole_grains_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["whole_grains_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["whole_grains_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["whole_grains_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_whole_grain"] = value
	if "refined_grains_consumption" in temp_user_profile:
		if temp_user_profile["refined_grains_consumption"][0] is not None:

			value = ""
			if temp_user_profile["refined_grains_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["refined_grains_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["refined_grains_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["refined_grains_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["refined_grains_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["refined_grains_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_refined_grain"] = value
	if "low_fat_dairy_consumption" in temp_user_profile:
		if temp_user_profile["low_fat_dairy_consumption"][0] is not None:

			value = ""
			if temp_user_profile["low_fat_dairy_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["low_fat_dairy_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["low_fat_dairy_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["low_fat_dairy_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["low_fat_dairy_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["low_fat_dairy_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_low_fat_dairy"] = value
	if "high_fat_dairy_saturated_fats_consumption" in temp_user_profile:
		if temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0] is not None:

			value = ""
			if temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["high_fat_dairy_saturated_fats_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_high_fat_dairy"] = value
	if "sweets_consumption" in temp_user_profile:
		if temp_user_profile["sweets_consumption"][0] is not None:

			value = ""
			if temp_user_profile["sweets_consumption"][0]["answer"] is None:
				value = temp_user_profile["option"]
			elif temp_user_profile["sweets_consumption"][0]["answer"] == "not_eat_at_all":
				value = "I do not eat it at all"
			elif temp_user_profile["sweets_consumption"][0]["answer"] == "less_than_1s_per_week":
				value = "Less than 1 serving per week"
			elif temp_user_profile["sweets_consumption"][0]["answer"] == "1-2_per_week":
				value = "1-2 servings per week"
			elif temp_user_profile["sweets_consumption"][0]["answer"] == "3-4_per_week":
				value = "3-4 servings per week"
			elif temp_user_profile["sweets_consumption"][0]["answer"] == "5-6_per_week":
				value = "5-6 servings per week"

			user_profile["how_often_sweets"] = value
	if "dietary_restriction_factors" in temp_user_profile:
		if temp_user_profile["dietary_restriction_factors"] is not None:
			for option in temp_user_profile["dietary_restriction_factors"]:
				if option["option"] is None:
					continue

				if option["answer"] == "definitely_limiting":
					value = 1
				elif option["answer"] == "somewhat_limiting":
					value = 2
				elif option["answer"] == "neither_limiting_nor_not_limiting":
					value = 3
				elif option["answer"] == "not_really_limiting":
					value = 4
				elif option["answer"] == "definitely_not_limiting":
					value = 5
				else:
					raise ValueError(f"Invalid dietary_restriction_factors value: {option['answer']}")

				if option["option"] is None:
					continue

				if option["option"] == "healthy_food_cost":
					user_profile["cost_of_healthy_food"] = value
				elif option["option"] == "fast_foods_high_availability":
					user_profile["high_availability_of_fast_food"] = value
				elif option["option"] == "limited_access":
					user_profile["lack_of_good_quality_food"] = value
				elif option["option"] == "lack_of_time":
					user_profile["lack_of_time"] = value
				elif option["option"] == "lack_of_support":
					user_profile["lack_of_support_from_family"] = value
				elif option["option"] == "local_community":
					user_profile["difficulty_in_avoiding_unhealthy_food_on_social_occasions"] = value
				elif option["option"] == "family_dietary_patterns":
					user_profile["unhealthy_family_eating_habits"] = value
				elif option["option"] == "healthcare_system_lack_of_support":
					user_profile["lack_of_support_from_healthcare_system"] = value
				elif option["option"] == "lack_of_knowledge_skills_lifestyle":
					user_profile["lack_of_knowledge_toward_healthier_life"] = value
				elif option["option"] == "lack_of_healthy_recommendations":
					user_profile["lack_of_knowledge_on_current_healthy_eating_recommendations"] = value
				elif option["option"] == "lack_of_meal_preparation":
					user_profile["lack_of_knowledge_on_healthy_food_preparation"] = value
				elif option["option"] == "healthy_eating_info_accuracy":
					user_profile["accuracy_of_healthy_eating_information"] = value
				elif option["option"] == "lot_of_effort":
					user_profile["lack_of_effort"] = value
				elif option["option"] == "temptations":
					user_profile["temptation_resistance"] = value
				elif option["option"] == "sweet_salty_craving":
					user_profile["craving"] = value
				elif option["option"] == "healthy_unfavourable":
					user_profile["dislike_of_healthy_food_taste"] = value
				elif option["option"] == "lack_of_motivation":
					user_profile["lack_of_motivation"] = value
				elif option["option"] == "lack_of_belief":
					user_profile["lack_of_healthy_food_preventing_disease"] = value
				else:
					raise ValueError(f"Invalid dietary_restriction_factors option: {option['option']}")
	if "dietary_support_factors" in temp_user_profile:
		if temp_user_profile["dietary_support_factors"] is not None:

			for option in temp_user_profile["dietary_support_factors"]:
				if option["answer"] == "definitely_not_enhancing":
					value = 1
				elif option["answer"] == "not_really_enhancing":
					value = 2
				elif option["answer"] == "neither_enhancing_nor_not_enhancing":
					value = 3
				elif option["answer"] == "somewhat_enhancing":
					value = 4
				elif option["answer"] == "definitely_enhancing":
					value = 5
				else:
					raise ValueError(f"Invalid dietary_support_factors value: {option['answer']}")

				if option["option"] is None:
					continue

				if option["option"] == "low_cost_healthy_food":
					user_profile["low_cost_of_healthy_food"] = value
				elif option["option"] == "access_to_fresh_low_calorie_foods":
					user_profile["accessibility_of_good_quality_food"] = value
				elif option["option"] == "income_mitigation_food_choices":
					user_profile["reduction_to_costs_of_healthy_food"] = value
				elif option["option"] == "food_preparation_help":
					user_profile["help_in_food_preparation"] = value
				elif option["option"] == "family_support_healthy_choices":
					user_profile["support_from_family"] = value
				elif option["option"] == "healthcare_emphasis_on_diet":
					user_profile["healthcare_professional_support"] = value
				elif option["option"] == "support_for_eating_recommendations":
					user_profile["support_of_knowledge_on_healthy_eating_recommendations"] = value
				elif option["option"] == "accountability_partner":
					user_profile["accountability_partner"] = value
				elif option["option"] == "collaboration_healthcare_team":
					user_profile["collaboration_with_healthcare_professionals"] = value
				elif option["option"] == "meal_preparation_skills":
					user_profile["skills_on_healthy_food_preparation"] = value
				elif option["option"] == "wake_up_call_diet_change":
					user_profile["wake_up_call"] = value
				elif option["option"] == "healthy_diet_routine_development":
					user_profile["development_of_routine"] = value
				elif option["option"] == "increased_energy_daily_life":
					user_profile["improvement_of_energy"] = value
				elif option["option"] == "role_modeling_healthy_diet":
					user_profile["role_model"] = value
	if "tobacco_use_history" in temp_user_profile:
		if temp_user_profile["tobacco_use_history"][0] is not None:
			if temp_user_profile["tobacco_use_history"][0]["answer"] == "never_smoked":
				user_profile["ever_smoked"] = "never"
			elif temp_user_profile["tobacco_use_history"][0]["answer"] == "former_smoker_gte_10":
				user_profile["ever_smoked"] = ">= 10 years"
			elif temp_user_profile["tobacco_use_history"][0]["answer"] == "former_smoker_lt_10":
				user_profile["ever_smoked"] = "< 10 years"
			elif temp_user_profile["tobacco_use_history"][0]["answer"] == "active_smoker":
				user_profile["ever_smoked"] = "active"
			else:
				raise ValueError(f"Invalid tobacco_use_history value: {temp_user_profile['tobacco_use_history']}")
	if "tobacco_use_duration" in temp_user_profile:
		if temp_user_profile["tobacco_use_duration"][0] is not None:
			if temp_user_profile["tobacco_use_duration"][0]["answer"] == "less_than_1":
				user_profile["duration_of_smoking"] = "< 1 year"
			elif temp_user_profile["tobacco_use_duration"][0]["answer"] == "2_to_5":
				user_profile["duration_of_smoking"] = "2-5 years"
			elif temp_user_profile["tobacco_use_duration"][0]["answer"] == "6_to_10":
				user_profile["duration_of_smoking"] = "6-10 years"
			elif temp_user_profile["tobacco_use_duration"][0]["answer"] == "more_than_10_years":
				user_profile["duration_of_smoking"] = ">10"
			else:
				raise ValueError(f"Invalid tobacco_use_duration value: {temp_user_profile['tobacco_use_duration']}")
	if "daily_tobacco_use" in temp_user_profile:
		if temp_user_profile["daily_tobacco_use"] is not None:
			for option in temp_user_profile["daily_tobacco_use"]:
				value = 0
				if option["answer"] is not None:
					value = int(option["answer"])

				if option["option"] == "manufactured_cigarettes":
					user_profile["manufactured_cigarettes"] = value
				elif option["option"] == "hand_rolled":
					user_profile["hand_rolled_cigarettes"] = value
				elif option["option"] == "pipes":
					user_profile["pipes"] = value
				elif option["option"] == "cigars_cheroots_cigarillos":
					user_profile["cigars"] = value
				elif option["option"] == "waterpipe":
					user_profile["water_pipe"] = value
				elif option["option"] == "other_number_per_day":
					user_profile["other_tobacco_products"] = value
				else:
					raise ValueError(f"Invalid daily_tobacco_use option: {option['option']}")
	if "vigorous_activity_days" in temp_user_profile:
		if temp_user_profile["vigorous_activity_days"] is not None:
			for option in temp_user_profile["vigorous_activity_days"]:
				if option["option"] != "number_of_days_per_week_all_vigorous_activities":
					continue

				value = 0
				if option["answer"] is not None:
					value = int(option["answer"])

				user_profile["vigorous_days_per_week"] = value
	if "vigorous_activity_duration" in temp_user_profile:
		if temp_user_profile["vigorous_activity_duration"] is not None:
			for option in temp_user_profile["vigorous_activity_duration"]:
				if option["option"] != "number_of_minutes_all_vigorous_per_day":
					continue

				value = 0
				if option["answer"] is not None:
					value = int(option["answer"])

				user_profile["vigorous_time_per_day"] = [value, "min"]
	if "moderate_activity_days" in temp_user_profile:
		if temp_user_profile["moderate_activity_days"] is not None:
			for option in temp_user_profile["moderate_activity_days"]:
				if option["option"] != "number_of_days_per_week_all_moderate_activities":
					continue

				value = 0
				if option["answer"] is not None:
					value = int(option["answer"])

				user_profile["moderate_days_per_week"] = value
	if "moderate_activity_duration" in temp_user_profile:
		if temp_user_profile["moderate_activity_duration"] is not None:
			for option in temp_user_profile["moderate_activity_duration"]:
				if option["option"] != "number_of_minutes_all_moderate_per_day":
					continue

				value = 0
				if option["answer"] is not None:
					value = int(option["answer"])

				user_profile["moderate_time_per_day"] = [value, "min"]
	if "walking_days_10_min" in temp_user_profile:
		if temp_user_profile["walking_days_10_min"][0] is not None:
			value = 0
			if temp_user_profile["walking_days_10_min"][0]["answer"] is not None:
				value = int(temp_user_profile["walking_days_10_min"][0]["answer"])

			user_profile["walking_days_per_week"] = value
	if "walking_duration" in temp_user_profile:
		if temp_user_profile["walking_duration"] is not None:
			value = 0
			if temp_user_profile["walking_duration"][0]["answer"] is not None:
				value = int(temp_user_profile["walking_duration"][0]["answer"])

			user_profile["walking_time_per_day"] = [value, "min"]
	# if "steps_per_day" in temp_user_profile:
	#     if temp_user_profile["steps_per_day"] is not None:
	if "sitting_time_weekday" in temp_user_profile:
		if temp_user_profile["sitting_time_weekday"] is not None:
			value = 0
			if temp_user_profile["sitting_time_weekday"][0]["answer"] is not None:
				value = int(temp_user_profile["sitting_time_weekday"][0]["answer"])

			user_profile["sitting_time_per_day"] = [value, "min"]
	if "activity_days_10_min" in temp_user_profile:
		if temp_user_profile["activity_days_10_min"] is not None:
			value = 0
			if temp_user_profile["activity_days_10_min"][0]["answer"] is not None:
				value = int(temp_user_profile["activity_days_10_min"][0]["answer"])

			user_profile["hobbies_days_per_week"] = value
	if "leisure_activity_duration" in temp_user_profile:
		if temp_user_profile["leisure_activity_duration"] is not None:
			value = 0
			if temp_user_profile["leisure_activity_duration"][0]["answer"] is not None:
				value = int(temp_user_profile["leisure_activity_duration"][0]["answer"])

			user_profile["hobbies_time_per_day"] = [value, "min"]
	if "walk_time_to_location" in temp_user_profile:
		if temp_user_profile["walk_time_to_location"] is not None:
			for option in temp_user_profile["walk_time_to_location"]:
				value = 0
				if option["answer"] == "less_than_10_min":
					value = "< 10 min"
				elif option["answer"] == "10_30_min":
					value = "10-30 min"
				elif option["answer"] == "more_than_30_min":
					value = "> 30 min"
				else:
					raise ValueError(f"Invalid walk_time_to_location value: {option['answer']}")

				if option["option"] == "park":
					user_profile["park_distance"] = value
				elif option["option"] == "open_gym":
					user_profile["open_gym_distance"] = value
				elif option["option"] == "gym":
					user_profile["gym_distance"] = value
				elif option["option"] == "pool":
					user_profile["pool_distance"] = value
	if "physical_activity_limitations" in temp_user_profile:
		if temp_user_profile["physical_activity_limitations"] is not None:
			for option in temp_user_profile["physical_activity_limitations"]:
				if option["answer"] == "definitely_limiting":
					value = 1
				elif option["answer"] == "somewhat_limiting":
					value = 2
				elif option["answer"] == "neither_limiting_nor_not_limiting":
					value = 3
				elif option["answer"] == "not_really_limiting":
					value = 4
				elif option["answer"] == "definitely_not_limiting":
					value = 5
				else:
					raise ValueError(f"Invalid physical_activity_limitations value: {option['answer']}")

				if option["option"] is None:
					continue

				if option["option"] == "lack_of_time_activity_limitations":
					user_profile["lack_of_time_for_physical_activity"] = value
				elif option["option"] == "lack_of_exercise_motivation":
					user_profile["lack_of_motivation_short_term"] = value
				elif option["option"] == "lack_of_long_term_motivation":
					user_profile["lack_of_motivation_long_term"] = value
				elif option["option"] == "fatigue_lack_of_energy":
					user_profile["feel_fatigue"] = value
				elif option["option"] == "sedentary_activity_competition":
					user_profile["sedentary_lifestyle"] = value
				elif option["option"] == "lack_of_healthcare_support":
					user_profile["lack_of_support_from_healthcare_professionals"] = value
				elif option["option"] == "lack_of_exercise_skills":
					user_profile["lack_of_exercising_skills"] = value
				elif option["option"] == "lack_of_physical_fitness":
					user_profile["lack_of_physical_fitness"] = value
				elif option["option"] == "concern_due_to_health":
					user_profile["concern_physical_condition"] = value
				elif option["option"] == "lack_of_support_network":
					user_profile["lack_of_support_from_family_physical_activity"] = value
				elif option["option"] == "lack_of_belief_in_effectiveness":
					user_profile["lack_of_physical_activity_preventing_disease"] = value
				elif option["option"] == "environmental_barriers":
					user_profile["lack_of_infrastructure"] = value
				elif option["option"] == "belief_health_is_sufficient":
					user_profile["delusion"] = value
				elif option["option"] == "lack_of_activity_knowledge":
					user_profile["lack_of_knowledge_on_physical_activity_recommendations"] = value
				elif option["option"] == "fear_of_injury":
					user_profile["fear_of_injury"] = value
				elif option["option"] == "social_norms_stigma":
					user_profile["stigma"] = value
				elif option["option"] == "weather_conditions_barrier":
					user_profile["weather_conditions"] = value
				elif option["option"] == "safety_concerns_exercise":
					user_profile["safety_concerns"] = value
				elif option["option"] == "discomfort_exercising_in_public":
					user_profile["uncomfortability"] = value
				elif option["option"] == "trust_in_activity_information":
					user_profile["accuracy_of_physical_activity_information"] = value
	if "physical_activity_enablers" in temp_user_profile:
		if temp_user_profile["physical_activity_enablers"] is not None:
			for option in temp_user_profile["physical_activity_enablers"]:
				if option["answer"] == "definitely_not_enhancing":
					value = 1
				elif option["answer"] == "not_really_enhancing":
					value = 2
				elif option["answer"] == "neither_enhancing_nor_not_enhancing":
					value = 3
				elif option["answer"] == "somewhat_enhancing":
					value = 4
				elif option["answer"] == "definitely_enhancing":
					value = 5
				else:
					raise ValueError(f"Invalid physical_activity_enablers value: {option['answer']}")

				if option["option"] is None:
					continue

				if option["option"] == "support_from_family_friends":
					user_profile["support_from_family_physical_activity"] = value
				elif option["option"] == "healthcare_emphasis_on_activity":
					user_profile["healthcare_professional_support_physical_activity"] = value
				elif option["option"] == "knowledge_of_activity_recommendations":
					user_profile["knowledge_on_physical_activity_recommendations"] = value
				elif option["option"] == "access_to_activity_options":
					user_profile["accessibility_of_physical_activity_infrastructure"] = value
				elif option["option"] == "exercise_routine_development":
					user_profile["development_of_routine_physical_activity"] = value
				elif option["option"] == "wake_up_call_diagnosis":
					user_profile["wake_up_call_physical_activity"] = value
				elif option["option"] == "role_modeling_exercise":
					user_profile["role_model_physical_activity"] = value
				elif option["option"] == "improved_energy_for_exercise":
					user_profile["improvement_of_energy_physical_activity"] = value
				elif option["option"] == "tailored_healthcare_support":
					user_profile["healthcare_professional_tailored_plan"] = value
	user_profile["alcohol_last_week"] = "none"
	user_profile["alcohol_last_week_per_day"] = "1-2"
	user_profile["alcohol_6_or_more_single_occasions"] = "none"
	print(f"Final User Profile")
	print(json5.dumps(user_profile, indent=4, quote_keys=True))
	with open("scrap/questionnaire_output.json", "w") as f:
		json5.dump(user_profile, f, indent=4, quote_keys=True)
	return user_profile