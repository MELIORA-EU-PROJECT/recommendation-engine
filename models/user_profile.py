from typing import List, Union, Optional

from pydantic import BaseModel


class BehaviorData(BaseModel):
	str: float
	ttm_stages: int


class DebugUserProfile(BaseModel):
	increase_physical_activity: BehaviorData
	improve_diet_quality: BehaviorData
	reduce_alcohol_consumption: BehaviorData
	cease_smoking: BehaviorData
	improve_mental_health: BehaviorData
	seek_medical_help: BehaviorData


class UserProfileSchema(BaseModel):
	year_of_birth: int
	ethnic_group: str
	country_of_origin: str
	current_country: str
	current_living_area: str
	marital_status: str
	highest_education: str
	current_employment: str
	household_economic_status: str
	caregiver: bool
	general_health: int
	height: float
	weight: float
	diagnosis: bool
	treatment_status: str
	cancer_free: bool
	chronic_condition: bool
	mental_condition: bool
	mental_conditions: Optional[List[str]] = None
	nervousness: int
	worryness: int
	depression: int
	uninterest: int
	pain: int
	fatigue: int
	nausea: int
	constipation: int
	disturbed_sleep: int
	shortness_of_breath: int
	lack_of_appetite: int
	drowsiness: int
	dry_mouth: int
	quality_of_life: int
	number_of_relatives_with_breast_cancer: str
	given_birth: bool
	current_menstrual_status: str
	breastfeeding: bool
	contraceptive_use: bool
	how_often_alcohol: str
	drinks_per_session: str
	how_often_6_or_more_drinks: str
	three_or_more_red_meat_weekly: bool
	how_often_fruit: str
	how_often_vegetables: str
	how_often_nuts: str
	how_often_fish: str
	how_often_whole_grain: str
	how_often_refined_grain: str
	how_often_low_fat_dairy: str
	how_often_high_fat_dairy: str
	how_often_sweets: str
	cost_of_healthy_food: int
	high_availability_of_fast_food: int
	lack_of_good_quality_food: int
	lack_of_time: int
	lack_of_support_from_family: int
	difficulty_in_avoiding_unhealthy_food_on_social_occasions: int
	unhealthy_family_eating_habits: int
	lack_of_support_from_healthcare_system: int
	lack_of_knowledge_toward_healthier_life: int
	lack_of_knowledge_on_current_healthy_eating_recommendations: int
	lack_of_knowledge_on_healthy_food_preparation: int
	accuracy_of_healthy_eating_information: int
	lack_of_effort: int
	temptation_resistance: int
	craving: int
	dislike_of_healthy_food_taste: int
	lack_of_motivation: int
	lack_of_healthy_food_preventing_disease: int
	low_cost_of_healthy_food: int
	accessibility_of_good_quality_food: int
	reduction_to_costs_of_healthy_food: int
	help_in_food_preparation: int
	support_from_family: int
	healthcare_professional_support: int
	support_of_knowledge_on_healthy_eating_recommendations: int
	accountability_partner: int
	collaboration_with_healthcare_professionals: int
	skills_on_healthy_food_preparation: int
	wake_up_call: int
	development_of_routine: int
	improvement_of_energy: int
	role_model: int
	ever_smoked: str
	duration_of_smoking: Optional[str] = None
	manufactured_cigarettes: int
	hand_rolled_cigarettes: int
	pipes: int
	cigars: int
	water_pipe: int
	other_tobacco_products: int
	vigorously_days_per_week: Optional[int] = None
	vigorously_time_per_day: Optional[List[Union[int, str]]] | str = None
	moderate_days_per_week: Optional[int] = None
	moderate_time_per_day: Optional[List[Union[int, str]]] | str = None
	sitting_time_per_day: Optional[List[Union[int, str]]] | str = None
	hobbies_days_per_week: Optional[int] = None
	hobbies_time_per_day: Optional[List[Union[int, str]]] | str = None
	park_distance: str
	open_gym_distance: str
	gym_distance: str
	pool_distance: str
	lack_of_time_for_physical_activity: int
	lack_of_motivation_short_term: int
	lack_of_motivation_long_term: int
	feel_fatigue: int
	sedentary_lifestyle: int
	lack_of_support_from_healthcare_professionals: int
	lack_of_exercising_skills: int
	lack_of_physical_fitness: int
	concern_physical_condition: int
	lack_of_support_from_family_physical_activity: int
	lack_of_physical_activity_preventing_disease: int
	lack_of_infrastructure: int
	delusion: int
	lack_of_knowledge_on_physical_activity_recommendations: int
	fear_of_injury: int
	stigma: int
	weather_conditions: int
	safety_concerns: int
	uncomfortability: int
	accuracy_of_physical_activity_information: int
	support_from_family_physical_activity: int
	healthcare_professional_support_physical_activity: int
	knowledge_on_physical_activity_recommendations: int
	accessibility_of_physical_activity_infrastructure: int
	development_of_routine_physical_activity: int
	wake_up_call_physical_activity: int
	role_model_physical_activity: int
	improvement_of_energy_physical_activity: int
	healthcare_professional_tailored_plan: int
	alcohol_last_week: str
	alcohol_last_week_per_day: str
	alcohol_6_or_more_single_occasions: str

	class Config:
		json_schema_extra = {
			"example":
				{
					"year_of_birth": 1980,
					"ethnic_group": "white",
					"country_of_origin": "Kenya",
					"current_country": "Spain",
					"current_living_area": "urban",
					"marital_status": "divorced",
					"highest_education": "master",
					"current_employment": "self-employed",
					"household_economic_status": "below average",
					"caregiver": True,
					"general_health": 3,
					"height": 1.736057601719263,
					"weight": 72.82147362203023,
					"diagnosis": False,
					"treatment_status": "no, completed",
					"cancer_free": False,
					"chronic_condition": False,
					"mental_condition": False,
					"nervousness": 1,
					"worryness": 3,
					"depression": 2,
					"uninterest": 2,
					"pain": 10,
					"fatigue": 5,
					"nausea": 7,
					"constipation": 2,
					"disturbed_sleep": 0,
					"shortness_of_breath": 8,
					"lack_of_appetite": 10,
					"drowsiness": 0,
					"dry_mouth": 10,
					"quality_of_life": 4,
					"number_of_relatives_with_breast_cancer": "one",
					"given_birth": False,
					"current_menstrual_status": "menopause",
					"breastfeeding": False,
					"contraceptive_use": False,
					"how_often_alcohol": "2-4 times per month",
					"drinks_per_session": "1-2",
					"how_often_6_or_more_drinks": "never",
					"three_or_more_red_meat_weekly": True,
					"how_often_fruit": "2-3 servings per day",
					"how_often_vegetables": "4-5 servings per day",
					"how_often_nuts": "2-3 servings per day",
					"how_often_fish": "2-3 servings per day",
					"how_often_whole_grain": "6 or more servings per day",
					"how_often_refined_grain": "6 or more servings per day",
					"how_often_low_fat_dairy": "2-3 servings per day",
					"how_often_high_fat_dairy": "3-4 servings per week",
					"how_often_sweets": "4-5 servings per day",
					"cost_of_healthy_food": 1,
					"high_availability_of_fast_food": 4,
					"lack_of_good_quality_food": 2,
					"lack_of_time": 4,
					"lack_of_support_from_family": 1,
					"difficulty_in_avoiding_unhealthy_food_on_social_occasions": 5,
					"unhealthy_family_eating_habits": 1,
					"lack_of_support_from_healthcare_system": 1,
					"lack_of_knowledge_toward_healthier_life": 4,
					"lack_of_knowledge_on_current_healthy_eating_recommendations": 5,
					"lack_of_knowledge_on_healthy_food_preparation": 3,
					"accuracy_of_healthy_eating_information": 1,
					"lack_of_effort": 2,
					"temptation_resistance": 2,
					"craving": 2,
					"dislike_of_healthy_food_taste": 2,
					"lack_of_motivation": 2,
					"lack_of_healthy_food_preventing_disease": 1,
					"low_cost_of_healthy_food": 2,
					"accessibility_of_good_quality_food": 2,
					"reduction_to_costs_of_healthy_food": 2,
					"help_in_food_preparation": 5,
					"support_from_family": 2,
					"healthcare_professional_support": 2,
					"support_of_knowledge_on_healthy_eating_recommendations": 2,
					"accountability_partner": 5,
					"collaboration_with_healthcare_professionals": 1,
					"skills_on_healthy_food_preparation": 4,
					"wake_up_call": 1,
					"development_of_routine": 3,
					"improvement_of_energy": 1,
					"role_model": 3,
					"ever_smoked": "never",
					"manufactured_cigarettes": 0,
					"hand_rolled_cigarettes": 0,
					"pipes": 0,
					"cigars": 0,
					"water_pipe": 0,
					"other_tobacco_products": 0,
					"moderate_days_per_week": 2,
					"moderate_time_per_day": [
						114,
						"min"
					],
					"sitting_time_per_day": [
						1,
						"hour"
					],
					"hobbies_days_per_week": 2,
					"hobbies_time_per_day": [
						1,
						"hour"
					],
					"park_distance": "> 30 min",
					"open_gym_distance": "10-30 min",
					"gym_distance": "> 30 min",
					"pool_distance": "10-30 min",
					"lack_of_time_for_physical_activity": 3,
					"lack_of_motivation_short_term": 2,
					"lack_of_motivation_long_term": 3,
					"feel_fatigue": 4,
					"sedentary_lifestyle": 5,
					"lack_of_support_from_healthcare_professionals": 4,
					"lack_of_exercising_skills": 4,
					"lack_of_physical_fitness": 1,
					"concern_physical_condition": 3,
					"lack_of_support_from_family_physical_activity": 4,
					"lack_of_physical_activity_preventing_disease": 5,
					"lack_of_infrastructure": 3,
					"delusion": 2,
					"lack_of_knowledge_on_physical_activity_recommendations": 4,
					"fear_of_injury": 1,
					"stigma": 4,
					"weather_conditions": 1,
					"safety_concerns": 3,
					"uncomfortability": 2,
					"accuracy_of_physical_activity_information": 1,
					"support_from_family_physical_activity": 3,
					"healthcare_professional_support_physical_activity": 2,
					"knowledge_on_physical_activity_recommendations": 4,
					"accessibility_of_physical_activity_infrastructure": 2,
					"development_of_routine_physical_activity": 4,
					"wake_up_call_physical_activity": 1,
					"role_model_physical_activity": 3,
					"improvement_of_energy_physical_activity": 5,
					"healthcare_professional_tailored_plan": 5,
					"alcohol_last_week": "1",
					"alcohol_last_week_per_day": "1-2",
					"alcohol_6_or_more_single_occasions": "1"
				}
		}