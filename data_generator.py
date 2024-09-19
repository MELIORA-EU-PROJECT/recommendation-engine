import random

import json5
import numpy as np

user_profile = {}
# READ TTM
# add more examples

# region "year_of_birth" - Lognormal Distribution ✅
distribution = np.random.lognormal(3, 0.6, 1000)
distribution = np.clip(distribution, 0, 100)
distribution = np.round(distribution)
distribution = distribution + 1950
distribution = distribution[distribution < 2005]
distribution = distribution.astype(int)
user_profile["year_of_birth"] = np.random.choice(distribution).item()
# endregion "year_of_birth" - Lognormal Distribution
# region "ethnic_group" - Random Choice from List ✅
ethnic_groups = ["white", "black", "hispanic", "asian", "mixed"]
user_profile["ethnic_group"] = random.choice(ethnic_groups)
# endregion "ethnic_group"
# region "country_of_origin" - Random Choice from List ✅
countries = ["USA", "UK", "Germany", "France", "Italy", "Spain", "Russia", "China", "Japan", "India", "Brazil",
             "Mexico", "Canada", "Australia", "South Africa", "Nigeria", "Egypt", "Kenya", "Ethiopia", "Ghana",
             "Morocco", "Tunisia", "Algeria", "Libya", "Sudan", "Uganda", "Angola", "Zimbabwe", "Zambia", "Mozambique",
             "Namibia", "Botswana", "Lesotho", "Swaziland", "Tanzania", "Rwanda", "Burundi", "Uganda", "Kenya",
             "Somalia", "Djibouti", "Eritrea", "Sudan", "South Sudan", "Central African Republic", "Chad", "Niger",
             "Mali", "Burkina Faso", "Senegal", "Gambia", "Guinea-Bissau", "Guinea", "Sierra Leone", "Liberia",
             "Ivory Coast", "Ghana", "Togo", "Benin", "Nigeria", "Cameroon", "Equatorial Guinea", "Gabon", "Congo",
             "Democratic Republic of the Congo", "Angola", "Namibia", "Botswana", "Zimbabwe", "Mozambique", "Malawi",
             "Zambia", "Tanzania", "Burundi", "Rwanda", "Uganda", "Kenya", "Somalia", "Djibouti", "Eritrea", "Sudan",
             "South Sudan", "Central African Republic", "Chad", "Niger", "Mali", "Burkina Faso", "Senegal", "Gambia",
             "Guinea-Bissau", "Guinea", "Sierra Leone", "Liberia", "Ivory Coast", "Ghana", "Togo", "Benin", "Nigeria",
             "Cameroon", "Equatorial Guinea", "Gabon", "Congo", "Democratic Republic of the Congo", "Angola", "Namibia",
             "Botswana", "Zimbabwe", "Mozambique", "Malawi", "Zambia", "Tanzania", "Burundi", "Rwanda", "Uganda", ]
user_profile["country_of_origin"] = random.choice(countries)
# endregion "country_of_origin"
# region "current_country" - Random Choice from List ✅
countries_of_study = ["Greece", "Lithuania", "Spain", "Sweden"]
user_profile["current_country"] = random.choice(countries_of_study)
# endregion "current_country"
# region "current_living_area" - Random Choice from List ✅
living_areas = ["urban", "suburban", "rural"]
user_profile["current_living_area"] = random.choice(living_areas)
# endregion "current_living_area"
# region "marital_status" - Random Choice from List ✅
marital_statuses = ["single", "married", "divorced", "widowed", "separated"]
user_profile["marital_status"] = random.choice(marital_statuses)
# endregion "marital_status"
# region "highest_education" - Random Choice from List ✅
educational_levels = ["no_education", "primary", "no high school diploma", "high school", "trade training", "bachelor",
                      "master", "phd"]
user_profile["highest_education"] = random.choice(educational_levels)
# endregion "highest_education"
# region "current_employment" - Random Choice from List ✅
employment_statuses = ["employed", "self-employed", "out of work", "homemaker", "student", "retired", "unable to work"]
user_profile["current_employment"] = random.choice(employment_statuses)
# endregion "current_employment"
# region "household_economic_status" - Random Choice from List ✅
household_economic_statuses = ["above average", "slightly above average", "average", "slightly below average",
                               "below average"]
user_profile["household_economic_status"] = random.choice(household_economic_statuses)
# endregion "household_economic_status"
# region "caregiver" - Bernoulli Distribution (30%) ✅
distribution = np.random.binomial(1, 0.3, 1000)
user_profile["caregiver"] = bool(np.random.choice(distribution) == 1)
# endregion "caregiver"
# region "general_health" - Normal Distribution ✅
distribution = np.random.normal(2, 1, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 4)
distribution = distribution.astype(int)
user_profile["general_health"] = np.random.choice(distribution).item()
# endregion "general_health"
# region "height" - Normal Distribution ✅
distribution = np.random.normal(1.7, 0.05, 1000)
distribution = np.clip(distribution, 1.4, 2)
user_profile["height"] = np.random.choice(distribution)
# endregion "height"
# region "weight" - Normal Distribution ✅
distribution = np.random.normal(70, 5, 1000)
distribution = distribution[distribution > 40]
distribution = distribution[distribution < 150]

user_profile["weight"] = np.random.choice(distribution)
# endregion "weight"
# region "diagnosis" - Bernoulli Distribution (50%) ✅
distribution = np.random.binomial(1, 0.5, 1000)
user_profile["diagnosis"] = bool(np.random.choice(distribution) == 1)
# endregion "diagnosis"
# region "first_diagnosis" - Lognormal Distribution for year - Uniform Distribution for month ✅
if user_profile["diagnosis"]:
    month = random.randint(1, 12)
    distribution = np.random.lognormal(3, 0.6, 1000)
    distribution = np.clip(distribution, 0, 100)
    distribution = np.round(distribution)
    distribution = distribution + 2000
    distribution = distribution[distribution < 2025]
    distribution = distribution.astype(int)
    year = np.random.choice(distribution)
    user_profile["first_diagnosis"] = f"{month:02}-{year}"
# endregion "first_diagnosis"
# region "treatment_status" - Random Choice from List ✅
treatment_statuses = ["no, completed", "yes", "no, waiting"]
if user_profile["diagnosis"]:
    user_profile["treatment_status"] = random.choice(treatment_statuses)
else:
    user_profile["treatment_status"] = "no, completed"
# endregion "treatment_status"
# region "treatment_type" - Random Choice from List ✅
if user_profile["treatment_status"] == "yes":
    treatment_types = ["surgery", "chemotherapy", "hormone therapy", "radiation therapy", "rehabilitation"]
    user_profile["treatment_type"] = random.choice(treatment_types)
# endregion "treatment_type"
# region "last_treatment" - Lognormal Distribution for year - Uniform Distribution for month ✅
if user_profile["treatment_status"] == "yes":
    month = random.randint(1, 12)
    distribution = np.random.lognormal(3, 0.6, 1000)
    distribution = np.clip(distribution, 0, 100)
    distribution = np.round(distribution)
    distribution = distribution + 2000
    distribution = distribution[distribution < 2025]
    distribution = distribution.astype(int)
    year = np.random.choice(distribution)
    user_profile["last_treatment"] = f"20-{month:02}-{year}"
# endregion "last_treatment"
# region "waiting_first_treatment" - Lognormal Distribution for year - Uniform Distribution for month ✅
if user_profile["treatment_status"] == "no, waiting":
    month = random.randint(1, 12)
    distribution = np.random.lognormal(3, 0.6, 1000)
    distribution = np.clip(distribution, 0, 100)
    distribution = np.round(distribution)
    distribution = distribution + 2000
    distribution = distribution[distribution < 2025]
    distribution = distribution.astype(int)
    year = np.random.choice(distribution)
    user_profile["waiting_first_treatment"] = f"20-{month:02}-{year}"
# endregion "waiting_first_treatment"
# region "cancer_free" - Bernoulli Distribution (10%) ✅
distribution = np.random.binomial(1, 0.1, 1000)
user_profile["cancer_free"] = bool(np.random.choice(distribution) == 1)
# endregion "cancer_free"
# region "chronic_condition" - Bernoulli Distribution (40%) ✅
distribution = np.random.binomial(1, 0.4, 1000)
user_profile["chronic_condition"] = bool(np.random.choice(distribution) == 1)
# endregion "chronic_condition"
# region "chronic_conditions" 🔴
# endregion "chronic_conditions"
# region "mental_condition" - Bernoulli Distribution (30%) ✅
distribution = np.random.binomial(1, 0.3, 1000)
user_profile["mental_condition"] = bool(np.random.choice(distribution) == 1)
# endregion "mental_condition"
# region "mental_conditions" - Random Choice from List ✅
mental_conditions = ["anxiety disorder", "bipolar disorder", "depression", "dissociation", "eating disorders",
                     "obsessive compulsive disorder", "paranoia", "post-traumatic stress disorder", "psychosis",
                     "schizophrenia"]

if user_profile["mental_condition"]:
    distribution = np.random.lognormal(3, 4, 1000)
    distribution = np.clip(distribution, 0, 10)
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    distribution = distribution + 1
    distribution = distribution[distribution < 11]
    number_of_mental_conditions = np.random.choice(distribution)

    user_profile["mental_conditions"] = random.sample(mental_conditions, k=number_of_mental_conditions)
# endregion "mental_conditions"
# region "nervousness" - Uniform Distribution ✅
user_profile["nervousness"] = random.randint(0, 3)
# endregion "nervousness"
# region "worryness" - Uniform Distribution ✅
user_profile["worryness"] = random.randint(0, 3)
# endregion "worryness"
# region "depression" - Uniform Distribution ✅
user_profile["depression"] = random.randint(0, 3)
# endregion "depression"
# region "uninterest" - Uniform Distribution ✅
user_profile["uninterest"] = random.randint(0, 3)
# endregion "uninterest"
# region "pain" - Uniform Distribution ✅
user_profile["pain"] = random.randint(0, 10)
# endregion "pain"
# region "fatigue" - Uniform Distribution ✅
user_profile["fatigue"] = random.randint(0, 10)
# endregion "fatigue"
# region "nausea" - Uniform Distribution ✅
user_profile["nausea"] = random.randint(0, 10)
# endregion "nausea"
# region "constipation" - Uniform Distribution ✅
user_profile["constipation"] = random.randint(0, 10)
# endregion "constipation"
# region "disturbed_sleep" - Uniform Distribution ✅
user_profile["disturbed_sleep"] = random.randint(0, 10)
# endregion "disturbed_sleep"
# region "shortness_of_breath" - Uniform Distribution ✅
user_profile["shortness_of_breath"] = random.randint(0, 10)
# endregion "shortness_of_breath"
# region "lack_of_appetite" - Uniform Distribution ✅
user_profile["lack_of_appetite"] = random.randint(0, 10)
# endregion "lack_of_appetite"
# region "drowsiness" - Uniform Distribution ✅
user_profile["drowsiness"] = random.randint(0, 10)
# endregion "drowsiness"
# region "dry_mouth" - Uniform Distribution ✅
user_profile["dry_mouth"] = random.randint(0, 10)
# endregion "dry_mouth"
# region "quality_of_life" - Uniform Distribution ✅
user_profile["quality_of_life"] = random.randint(0, 4)
# endregion "quality_of_life"
# region "number_of_relatives_with_breast_cancer" - Random Choice from List ✅
numbers_first_choices = ["none", "one", "more than one", "unknown"]
user_profile["number_of_relatives_with_breast_cancer"] = random.choice(numbers_first_choices)
# endregion "number_of_relatives_with_breast_cancer"
# region "given_birth" - Bernoulli Distribution (50%) ✅
distribution = np.random.binomial(1, 0.5, 1000)
user_profile["given_birth"] = bool(np.random.choice(distribution) == 1)
# endregion "given_birth"
# region "current_menstrual_status" - Random Choice from List ✅
menstrual_statuses = ["premenopause", "perimenopause", "menopause"]
user_profile["current_menstrual_status"] = random.choice(menstrual_statuses)
# endregion "current_menstrual_status"
# region "breastfeeding" - Bernoulli Distribution (80%) ✅
if user_profile["given_birth"]:
    distribution = np.random.binomial(1, 0.8, 1000)
    user_profile["breastfeeding"] = bool(np.random.choice(distribution) == 1)
else:
    user_profile["breastfeeding"] = False
# endregion "breastfeeding"
# region "contraceptive_use" - Bernoulli Distribution (50%) ✅
distribution = np.random.binomial(1, 0.5, 1000)
user_profile["contraceptive_use"] = bool(np.random.choice(distribution) == 1)
# endregion "contraceptive_use"
# region "how_often_alcohol" - Random Choice from List ✅
alcohol_frequencies = ["never", "monthly or less", "2-4 times per month", "2-3 times per week",
                       "4 or more times per week"]
user_profile["how_often_alcohol"] = random.choice(alcohol_frequencies)
# endregion "how_often_alcohol"
# region "drinks_per_session" - Random Choice from List ✅
drinks_per_sessions = ["1-2", "3-4", "5-6", "7-9", "10 or more"]
user_profile["drinks_per_session"] = random.choice(drinks_per_sessions)
# endregion "drinks_per_session"
# region "how_often_6_or_more_drinks" - Random Choice from List ✅
how_often_6_or_more_drinks = ["never", "less than monthly", "monthly", "weekly", "daily or almost daily"]
user_profile["how_often_6_or_more_drinks"] = random.choice(how_often_6_or_more_drinks)
# endregion "how_often_6_or_more_drinks"
# region "3_or_more_red_meat_weekly" - Bernoulli Distribution (70%) ✅
distribution = np.random.binomial(1, 0.7, 1000)
user_profile["3_or_more_red_meat_weekly"] = bool(np.random.choice(distribution) == 1)
# endregion "3_or_more_red_meat_weekly"
# region "how_often_fruit" - Random Choice from List ✅
fruit_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                     "3-4 servings per week", "5-6 servings per week", "1 serving per day", "2-3 servings per day",
                     "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_fruit"] = random.choice(fruit_frequencies)
# endregion "how_often_fruit"
# region "how_often_vegetables" - Random Choice from List ✅
vegetable_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                         "3-4 servings per week", "5-6 servings per week", "1 serving per day", "2-3 servings per day",
                         "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_vegetables"] = random.choice(vegetable_frequencies)
# endregion "how_often_vegetables"
# region "how_often_nuts" - Random Choice from List ✅
nuts_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                    "3-4 servings per week", "5-6 servings per week", "1 serving per day", "2-3 servings per day",
                    "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_nuts"] = random.choice(nuts_frequencies)
# endregion "how_often_nuts"
# region "how_often_fish" - Random Choice from List ✅
fish_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                    "3-4 servings per week", "5-6 servings per week", "1 serving per day", "2-3 servings per day",
                    "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_fish"] = random.choice(fish_frequencies)
# endregion "how_often_fish"
# region "how_often_whole_grain" - Random Choice from List ✅
whole_grain_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                           "3-4 servings per week", "5-6 servings per week", "1 serving per day",
                           "2-3 servings per day",
                           "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_whole_grain"] = random.choice(whole_grain_frequencies)
# endregion "how_often_whole_grain"
# region "how_often_refined_grain" - Random Choice from List ✅
refined_grain_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                             "3-4 servings per week", "5-6 servings per week", "1 serving per day",
                             "2-3 servings per day", "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_refined_grain"] = random.choice(refined_grain_frequencies)
# endregion "how_often_refined_grain"
# region "how_often_low_fat_dairy" - Random Choice from List ✅
low_fat_dairy_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                             "3-4 servings per week", "5-6 servings per week", "1 serving per day",
                             "2-3 servings per day", "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_low_fat_dairy"] = random.choice(low_fat_dairy_frequencies)
# endregion "how_often_low_fat_dairy"
# region "how_often_high_fat_dairy" - Random Choice from List ✅
high_fat_dairy_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                              "3-4 servings per week", "5-6 servings per week", "1 serving per day",
                              "2-3 servings per day", "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_high_fat_dairy"] = random.choice(high_fat_dairy_frequencies)
# endregion "how_often_high_fat_dairy"
# region "how_often_sweets" - Random Choice from List ✅
sweets_frequencies = ["I do not eat it at all", "Less than 1 serving per week", "1-2 servings per week",
                      "3-4 servings per week", "5-6 servings per week", "1 serving per day", "2-3 servings per day",
                      "4-5 servings per day", "6 or more servings per day"]
user_profile["how_often_sweets"] = random.choice(sweets_frequencies)
# endregion "how_often_sweets"
# region "cost_of_healthy_food" - Uniform Distribution ✅
user_profile["cost_of_healthy_food"] = random.randint(1, 5)
# endregion "cost_of_healthy_food"
# region "high_availability_of_fast_food" - Uniform Distribution ✅
user_profile["high_availability_of_fast_food"] = random.randint(1, 5)
# endregion "high_availability_of_fast_food"
# region "lack_of_good_quality_food" - Uniform Distribution ✅
user_profile["lack_of_good_quality_food"] = random.randint(1, 5)
# endregion "lack_of_good_quality_food"
# region "lack_of_time" - Uniform Distribution ✅
user_profile["lack_of_time"] = random.randint(1, 5)
# endregion "lack_of_time"
# region "lack_of_support_from_family" - Uniform Distribution ✅
user_profile["lack_of_support_from_family"] = random.randint(1, 5)
# endregion "lack_of_support_from_family"
# region "difficulty_in_avoiding_unhealthy_food_on_social_occasions" - Uniform Distribution ✅
user_profile["difficulty_in_avoiding_unhealthy_food_on_social_occasions"] = random.randint(1, 5)
# endregion "difficulty_in_avoiding_unhealthy_food_on_social_occasions"
# region "unhealthy_family_eating_habits" - Uniform Distribution ✅
user_profile["unhealthy_family_eating_habits"] = random.randint(1, 5)
# endregion "unhealthy_family_eating_habits"
# region "lack_of_support_from_healthcare_system" - Uniform Distribution ✅
user_profile["lack_of_support_from_healthcare_system"] = random.randint(1, 5)
# endregion "lack_of_support_from_healthcare_system"
# region "lack_of_knowledge_toward_healthier_life" - Uniform Distribution ✅
user_profile["lack_of_knowledge_toward_healthier_life"] = random.randint(1, 5)
# endregion "lack_of_knowledge_toward_healthier_life"
# region "lack_of_knowledge_on_current_healthy_eating_recommendations" - Uniform Distribution ✅
user_profile["lack_of_knowledge_on_current_healthy_eating_recommendations"] = random.randint(1, 5)
# endregion "lack_of_knowledge_on_current_healthy_eating_recommendations"
# region "lack_of_knowledge_on_healthy_food_preparation" - Uniform Distribution ✅
user_profile["lack_of_knowledge_on_healthy_food_preparation"] = random.randint(1, 5)
# endregion "lack_of_knowledge_on_healthy_food_preparation"
# region "accuracy_of_healthy_eating_information" - Uniform Distribution ✅
user_profile["accuracy_of_healthy_eating_information"] = random.randint(1, 5)
# endregion "accuracy_of_healthy_eating_information"
# region "lack_of_effort" - Uniform Distribution ✅
user_profile["lack_of_effort"] = random.randint(1, 5)
# endregion "lack_of_effort"
# region "temptation_resistance" - Uniform Distribution ✅
user_profile["temptation_resistance"] = random.randint(1, 5)
# endregion "temptation_resistance"
# region "craving" - Uniform Distribution ✅
user_profile["craving"] = random.randint(1, 5)
# endregion "craving"
# region "dislike_of_healthy_food_taste" - Uniform Distribution ✅
user_profile["dislike_of_healthy_food_taste"] = random.randint(1, 5)
# endregion "dislike_of_healthy_food_taste"
# region "lack_of_motivation" - Uniform Distribution ✅
user_profile["lack_of_motivation"] = random.randint(1, 5)
# endregion "lack_of_motivation"
# region "lack_of_healthy_food_preventing_disease" - Uniform Distribution ✅
user_profile["lack_of_healthy_food_preventing_disease"] = random.randint(1, 5)
# endregion "lack_of_healthy_food_preventing_disease"
# region "low_cost_of_healthy_food" - Uniform Distribution ✅
user_profile["low_cost_of_healthy_food"] = random.randint(1, 5)
# endregion "low_cost_of_healthy_food"
# region "accessibility_of_good_quality_food" - Uniform Distribution ✅
user_profile["accessibility_of_good_quality_food"] = random.randint(1, 5)
# endregion "accessibility_of_good_quality_food"
# region "reduction_to_costs_of_healthy_food" - Uniform Distribution ✅
user_profile["reduction_to_costs_of_healthy_food"] = random.randint(1, 5)
# endregion "reduction_to_costs_of_healthy_food"
# region "help_in_food_preparation" - Uniform Distribution ✅
user_profile["help_in_food_preparation"] = random.randint(1, 5)
# endregion "help_in_food_preparation"
# region "support_from_family" - Uniform Distribution ✅
user_profile["support_from_family"] = random.randint(1, 5)
# endregion "support_from_family"
# region "healthcare_professional_support" - Uniform Distribution ✅
user_profile["healthcare_professional_support"] = random.randint(1, 5)
# endregion "healthcare_professional_support"
# region "support_of_knowledge_on_healthy_eating_recommendations" - Uniform Distribution ✅
user_profile["support_of_knowledge_on_healthy_eating_recommendations"] = random.randint(1, 5)
# endregion "support_of_knowledge_on_healthy_eating_recommendations"
# region "accountability_partner" - Uniform Distribution ✅
user_profile["accountability_partner"] = random.randint(1, 5)
# endregion "accountability_partner"
# region "collaboration_with_healthcare_professionals" - Uniform Distribution ✅
user_profile["collaboration_with_healthcare_professionals"] = random.randint(1, 5)
# endregion "collaboration_with_healthcare_professionals"
# region "skills_on_healthy_food_preparation" - Uniform Distribution ✅
user_profile["skills_on_healthy_food_preparation"] = random.randint(1, 5)
# endregion "skills_on_healthy_food_preparation"
# region "wake_up_call" - Uniform Distribution ✅
user_profile["wake_up_call"] = random.randint(1, 5)
# endregion "wake_up_call"
# region "development_of_routine" - Uniform Distribution ✅
user_profile["development_of_routine"] = random.randint(1, 5)
# endregion "development_of_routine"
# region "improvement_of_energy" - Uniform Distribution ✅
user_profile["improvement_of_energy"] = random.randint(1, 5)
# endregion "improvement_of_energy"
# region "role_model" - Uniform Distribution ✅
user_profile["role_model"] = random.randint(1, 5)
# endregion "role_model"
# region "ever_smoked" - Random Choice from List ✅
smoking_statuses = ["never", ">= 10 years", "< 10 years", "active"]
user_profile["ever_smoked"] = random.choice(smoking_statuses)
# endregion "ever_smoked"
# region "duration_of_smoking" - Random Choice from List ✅
if user_profile["ever_smoked"] != "never":
    smoking_durations = ["< 1 year", "2-5 years", "6-10 years", ">10"]
    user_profile["duration_of_smoking"] = random.choice(smoking_durations)
# endregion "duration_of_smoking"
# region "manufactured_cigarettes" - Lognormal Distribution ✅
if user_profile["ever_smoked"] == "active":
    distribution = np.random.lognormal(1, 1, 1000)
    distribution = distribution[distribution < 50]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["manufactured_cigarettes"] = np.random.choice(distribution).item()
else:
    user_profile["manufactured_cigarettes"] = 0
# endregion "manufactured_cigarettes"
# region "hand_rolled_cigarettes" - Lognormal Distribution ✅
if user_profile["ever_smoked"] == "active":
    distribution = np.random.lognormal(1, 1, 1000)
    distribution = distribution[distribution < 50]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["hand_rolled_cigarettes"] = np.random.choice(distribution).item()
else:
    user_profile["hand_rolled_cigarettes"] = 0
# endregion "hand_rolled_cigarettes"
# region "pipes" - Lognormal Distribution ✅
if user_profile["ever_smoked"] == "active":
    distribution = np.random.lognormal(1, 1, 1000)
    distribution = distribution[distribution < 50]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["pipes"] = np.random.choice(distribution).item()
else:
    user_profile["pipes"] = 0
# endregion "pipes"
# region "cigars" - Lognormal Distribution ✅
if user_profile["ever_smoked"] == "active":
    distribution = np.random.lognormal(1, 1, 1000)
    distribution = distribution[distribution < 50]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["cigars"] = np.random.choice(distribution).item()
else:
    user_profile["cigars"] = 0
# endregion "cigars"
# region "water_pipe" - Lognormal Distribution ✅
if user_profile["ever_smoked"] == "active":
    distribution = np.random.lognormal(1, 1, 1000)
    distribution = distribution[distribution < 50]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["water_pipe"] = np.random.choice(distribution).item()
else:
    user_profile["water_pipe"] = 0
# endregion "water_pipe"
# region "other_tobacco_products" - Lognormal Distribution ✅
if user_profile["ever_smoked"] == "active":
    distribution = np.random.lognormal(1, 1, 1000)
    distribution = distribution[distribution < 50]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["other_tobacco_products"] = np.random.choice(distribution).item()
else:
    user_profile["other_tobacco_products"] = 0
# endregion "other_tobacco_products"
# region "vigorous_days_per_week" - Powerlaw Distribution ✅
do_vigorous_activity = random.randint(0, 1)
if do_vigorous_activity:
    distribution = np.random.pareto(2, 1000)
    distribution = distribution + 1
    distribution = distribution[distribution < 5]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["vigorous_days_per_week"] = np.random.choice(distribution).item()
# endregion "vigorous_days_per_week"
# region "vigorous_time_per_day" - Powerlaw Distribution for Hours - Lognormal Distribution for Minutes ✅
if "vigorous_days_per_week" in user_profile:
    knows_activity = np.random.binomial(1, 0.95, 1000)
    knows_activity = np.random.choice(knows_activity)
    if knows_activity:
        hours_true_minutes_false = random.randint(0, 1)
        if hours_true_minutes_false:
            distribution = np.random.pareto(2.5, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 5]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["vigorous_time_per_day"] = [np.random.choice(distribution).item(), "hour"]
        else:
            distribution = np.random.lognormal(3, 0.6, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 160]
            distribution = distribution[distribution > 10]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["vigorous_time_per_day"] = [np.random.choice(distribution).item(), "min"]
    else:
        user_profile["vigorous_time_per_day"] = "don't know"
# endregion "vigorous_time_per_day"
# region "moderate_days_per_week" - Powerlaw Distribution ✅
do_moderate_activity = random.randint(0, 1)
if do_moderate_activity:
    distribution = np.random.pareto(2, 1000)
    distribution = distribution + 1
    distribution = distribution[distribution < 5]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["moderate_days_per_week"] = np.random.choice(distribution).item()

# endregion "moderate_days_per_week"
# region "moderate_time_per_day" - Powerlaw Distribution for Hours - Lognormal Distribution for Minutes ✅
if "moderate_days_per_week" in user_profile:
    knows_activity = np.random.binomial(1, 0.95, 1000)
    knows_activity = np.random.choice(knows_activity)
    if knows_activity:
        hours_true_minutes_false = random.randint(0, 1)
        if hours_true_minutes_false:
            distribution = np.random.pareto(2.5, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 5]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["moderate_time_per_day"] = [np.random.choice(distribution).item(), "hour"]
        else:
            distribution = np.random.lognormal(3, 0.6, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 160]
            distribution = distribution[distribution > 10]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["moderate_time_per_day"] = [np.random.choice(distribution).item(), "min"]
    else:
        user_profile["moderate_time_per_day"] = "don't know"

# endregion "moderate_time_per_day"
# region "walking_days_per_week" - Powerlaw Distribution ✅
do_walking_activity = random.randint(0, 1)
if do_walking_activity:
    distribution = np.random.pareto(2, 1000)
    distribution = distribution + 1
    distribution = distribution[distribution < 5]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["walking_days_per_week"] = np.random.choice(distribution).item()

# endregion "walking_days_per_week"
# region "walking_time_per_day" - Powerlaw Distribution for Hours - Lognormal Distribution for Minutes ✅
if "walking_days_per_week" in user_profile:
    knows_activity = np.random.binomial(1, 0.95, 1000)
    knows_activity = np.random.choice(knows_activity)
    if knows_activity:
        hours_true_minutes_false = random.randint(0, 1)
        if hours_true_minutes_false:
            distribution = np.random.pareto(2.5, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 5]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["walking_time_per_day"] = [np.random.choice(distribution).item(), "hour"]
        else:
            distribution = np.random.lognormal(3, 0.6, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 160]
            distribution = distribution[distribution > 10]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["walking_time_per_day"] = [np.random.choice(distribution).item(), "min"]
    else:
        user_profile["walking_time_per_day"] = "don't know"

# endregion "walking_time_per_day"
# region "sitting_time_per_day" - Powerlaw Distribution for Hours - Lognormal Distribution for Minutes ✅
knows_activity = np.random.binomial(1, 0.95, 1000)
knows_activity = np.random.choice(knows_activity)
if knows_activity:
    hours_true_minutes_false = random.randint(0, 1)
    if hours_true_minutes_false:
        distribution = np.random.pareto(2.5, 1000)
        distribution = distribution + 1
        distribution = distribution[distribution < 5]
        distribution = np.round(distribution)
        distribution = distribution.astype(int)
        user_profile["sitting_time_per_day"] = [np.random.choice(distribution).item(), "hour"]
    else:
        distribution = np.random.lognormal(3, 0.6, 1000)
        distribution = distribution + 1
        distribution = distribution[distribution < 160]
        distribution = distribution[distribution > 10]
        distribution = np.round(distribution)
        distribution = distribution.astype(int)
        user_profile["sitting_time_per_day"] = [np.random.choice(distribution).item(), "min"]
else:
    user_profile["sitting_time_per_day"] = "don't know"
# endregion "sitting_time_per_day"
# region "hobbies_days_per_week" - Powerlaw Distribution ✅
do_hobbies_activity = random.randint(0, 1)
if do_hobbies_activity:
    distribution = np.random.pareto(2, 1000)
    distribution = distribution + 1
    distribution = distribution[distribution < 5]
    distribution = np.round(distribution)
    distribution = distribution.astype(int)
    user_profile["hobbies_days_per_week"] = np.random.choice(distribution).item()
# endregion "hobbies_days_per_week"
# region "hobbies_time_per_day" - Powerlaw Distribution for Hours - Lognormal Distribution for Minutes ✅
if "hobbies_days_per_week" in user_profile:
    knows_activity = np.random.binomial(1, 0.95, 1000)
    knows_activity = np.random.choice(knows_activity)
    if knows_activity:
        hours_true_minutes_false = random.randint(0, 1)
        if hours_true_minutes_false:
            distribution = np.random.pareto(2.5, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 5]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["hobbies_time_per_day"] = [np.random.choice(distribution).item(), "hour"]
        else:
            distribution = np.random.lognormal(3, 0.6, 1000)
            distribution = distribution + 1
            distribution = distribution[distribution < 160]
            distribution = distribution[distribution > 10]
            distribution = np.round(distribution)
            distribution = distribution.astype(int)
            user_profile["hobbies_time_per_day"] = [np.random.choice(distribution).item(), "min"]
    else:
        user_profile["hobbies_time_per_day"] = "don't know"
# endregion "hobbies_time_per_day"
# region "park_distance" - Random Choice from List ✅
distances = ["< 10 min", "10-30 min", "> 30 min"]
user_profile["park_distance"] = random.choice(distances)
# endregion "park_distance"
# region "open_gym_distance" - Random Choice from List ✅
user_profile["open_gym_distance"] = random.choice(distances)
# endregion "open_gym_distance"
# region "gym_distance" - Random Choice from List ✅
user_profile["gym_distance"] = random.choice(distances)
# endregion "gym_distance"
# region "pool_distance" - Random Choice from List ✅
user_profile["pool_distance"] = random.choice(distances)
# endregion "pool_distance"
# region "lack_of_time_for_physical_activity" - Uniform Distribution ✅
user_profile["lack_of_time_for_physical_activity"] = random.randint(1, 5)
# endregion "lack_of_time_for_physical_activity"
# region "lack_of_motivation_short_term" - Uniform Distribution ✅
user_profile["lack_of_motivation_short_term"] = random.randint(1, 5)
# endregion "lack_of_motivation_short_term"
# region "lack_of_motivation_long_term" - Uniform Distribution ✅
user_profile["lack_of_motivation_long_term"] = random.randint(1, 5)
# endregion "lack_of_motivation_long_term"
# region "feel_fatigue" - Uniform Distribution ✅
user_profile["feel_fatigue"] = random.randint(1, 5)
# endregion "feel_fatigue"
# region "sedentary_lifestyle" - Uniform Distribution ✅
user_profile["sedentary_lifestyle"] = random.randint(1, 5)
# endregion "sedentary_lifestyle"
# region "lack_of_support_from_healthcare_professionals" - Uniform Distribution ✅
user_profile["lack_of_support_from_healthcare_professionals"] = random.randint(1, 5)
# endregion "lack_of_support_from_healthcare_professionals"
# region "lack_of_exercising_skills" - Uniform Distribution ✅
user_profile["lack_of_exercising_skills"] = random.randint(1, 5)
# endregion "lack_of_exercising_skills"
# region "lack_of_physical_fitness" - Uniform Distribution ✅
user_profile["lack_of_physical_fitness"] = random.randint(1, 5)
# endregion "lack_of_physical_fitness"
# region "concern_physical_condition" - Uniform Distribution ✅
user_profile["concern_physical_condition"] = random.randint(1, 5)
# endregion "concern_physical_condition"
# region "lack_of_support_from_family_physical_activity" - Uniform Distribution ✅
user_profile["lack_of_support_from_family_physical_activity"] = random.randint(1, 5)
# endregion "lack_of_support_from_family_physical_activity"
# region "lack_of_physical_activity_preventing_disease" - Uniform Distribution ✅
user_profile["lack_of_physical_activity_preventing_disease"] = random.randint(1, 5)
# endregion "lack_of_physical_activity_preventing_disease"
# region "lack_of_infrastructure" - Uniform Distribution ✅
user_profile["lack_of_infrastructure"] = random.randint(1, 5)
# endregion "lack_of_infrastructure"
# region "delusion" - Uniform Distribution ✅
user_profile["delusion"] = random.randint(1, 5)
# endregion "delusion"
# region "lack_of_knowledge_on_physical_activity_recommendations" - Uniform Distribution ✅
user_profile["lack_of_knowledge_on_physical_activity_recommendations"] = random.randint(1, 5)
# endregion "lack_of_knowledge_on_physical_activity_recommendations"
# region "fear_of_injury" - Uniform Distribution ✅
user_profile["fear_of_injury"] = random.randint(1, 5)
# endregion "fear_of_injury"
# region "stigma" - Uniform Distribution ✅
user_profile["stigma"] = random.randint(1, 5)
# endregion "stigma"
# region "weather_conditions" - Uniform Distribution ✅
user_profile["weather_conditions"] = random.randint(1, 5)
# endregion "weather_conditions"
# region "safety_concerns" - Uniform Distribution ✅
user_profile["safety_concerns"] = random.randint(1, 5)
# endregion "safety_concerns"
# region "uncomfortability" - Uniform Distribution ✅
user_profile["uncomfortability"] = random.randint(1, 5)
# endregion "uncomfortability"
# region "accuracy_of_physical_activity_information" - Uniform Distribution ✅
user_profile["accuracy_of_physical_activity_information"] = random.randint(1, 5)
# endregion "accuracy_of_physical_activity_information"
# region "support_from_family_physical_activity" - Uniform Distribution ✅
user_profile["support_from_family_physical_activity"] = random.randint(1, 5)
# endregion "support_from_family_physical_activity"
# region "healthcare_professional_support_physical_activity" - Uniform Distribution ✅
user_profile["healthcare_professional_support_physical_activity"] = random.randint(1, 5)
# endregion "healthcare_professional_support_physical_activity"
# region "knowledge_on_physical_activity_recommendations" - Uniform Distribution ✅
user_profile["knowledge_on_physical_activity_recommendations"] = random.randint(1, 5)
# endregion "knowledge_on_physical_activity_recommendations"
# region "accessibility_of_physical_activity_infrastructure" - Uniform Distribution ✅
user_profile["accessibility_of_physical_activity_infrastructure"] = random.randint(1, 5)
# endregion "accessibility_of_physical_activity_infrastructure"
# region "development_of_routine_physical_activity" - Uniform Distribution ✅
user_profile["development_of_routine_physical_activity"] = random.randint(1, 5)
# endregion "development_of_routine_physical_activity"
# region "wake_up_call_physical_activity" - Uniform Distribution ✅
user_profile["wake_up_call_physical_activity"] = random.randint(1, 5)
# endregion "wake_up_call_physical_activity"
# region "role_model_physical_activity" - Uniform Distribution ✅
user_profile["role_model_physical_activity"] = random.randint(1, 5)
# endregion "role_model_physical_activity"
# region "improvement_of_energy_physical_activity" - Uniform Distribution ✅
user_profile["improvement_of_energy_physical_activity"] = random.randint(1, 5)
# endregion "improvement_of_energy_physical_activity"
# region "healthcare_professional_tailored_plan" - Uniform Distribution ✅
user_profile["healthcare_professional_tailored_plan"] = random.randint(1, 5)
# endregion "healthcare_professional_tailored_plan"
# region "alcohol_last_week" - Random Choice from List ✅
alcohol_last_week_choices = ["none", "1", "2-3", "4 or more"]
user_profile["alcohol_last_week"] = random.choice(alcohol_last_week_choices)
# endregion "alcohol_last_week"
# region "alcohol_last_week_per_day" - Random Choice from List ✅
alcohol_last_week_per_day_choices = ["1-2", "3-4", "5-6", "7-9", "10 or more"]
user_profile["alcohol_last_week_per_day"] = random.choice(alcohol_last_week_per_day_choices)
# endregion "alcohol_last_week_per_day"
# region "alcohol_6_or_more_single_occasions" - Random Choice from List ✅
alcohol_6_or_more_single_occasions_choices = ["none", "1", "2-3", "4-5", "daily or almost daily"]
user_profile["alcohol_6_or_more_single_occasions"] = random.choice(alcohol_6_or_more_single_occasions_choices)
# endregion "alcohol_6_or_more_single_occasions"

# TODO PAPER
# RELATED WORK + INTRO
# 4 PAPERS ON CAUSALITY
# CREATE A DUMMY GRAPH AND TRY TO INTEGRATE IT IN THE PROGRAM
# DOWHY framework,GraphViz,
# write a simple explantation of dag integration in the TTM
import requests

url = f"http://localhost:8000/"
print(f"Sending data to {url}")
print(f"Data: {user_profile}")
print(f"to json: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
response = requests.post(url, json=user_profile)

json_response = response.json()
print(f"Response: {json5.dumps(json_response, indent=4, quote_keys=True)}")