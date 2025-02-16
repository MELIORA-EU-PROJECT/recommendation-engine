"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""
from typing import List

import json5
import uvicorn

from models.mini_course import MiniCourseScheduleAndEducationalMaterialsResponse
from models.recommendation import Recommendation
from models.user_profile import UserProfileSchema
from models.util_models import DebugResponse, DayResponse
from utils import *

from fastapi import FastAPI, Request, Response, HTTPException

from dotenv import load_dotenv
from colorama import init as colorama_init
from colorama import Fore, Style

colorama_init()
load_dotenv()

app = FastAPI()


@app.get("/",
		 summary="A simple health check endpoint",
		 tags=["health-check"],
		 responses={
			 200: {
				 "description": "Health check successful",
				 "content": {
					 "application/json": {
						 "example": {"Hello": "World"}
					 }
				 }
			 }
		 })
def read_root():
	return {"Hello": "World"}


@app.get("/v2/recommend/{userId}",
		 summary="Get recommendations for a userId (main endpoint)",
		 response_model=List[Recommendation],
		 tags=["v2"],
		 responses={
			 200: {
				 "description": "Recommendations for the userId",
				 "content": {
					 "application/json": {
						 "example": [
							 {"title": "Article 1", "recommendation_value": 0.5},
							 {"title": "Article 2", "recommendation_value": 0.3},
							 {"title": "Article 3", "recommendation_value": 0.1},
						 ]
					 }
				 }
			 },
			 500: {
				 "description": "Internal server error",
				 "content": {
					 "application/json": {
						 "example": {
							 "error": "There was an error retrieving the user profile"
						 }
					 }
				 }
			 }
		 })
async def recommendV2(userId: str, response: Response):
	# TODO: implement 0 result handling
	user_profile = create_user_profile(userId)

	# TODO: handle missing userId and Database-connection errors differently
	if not user_profile:
		response.status_code = 500
		return {"error": "There was an error retrieving the user profile"}

	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	full_recommendations = get_recommendations(user_profile)
	recommendations = [{"title": rec["title"], "recommendation_value": rec["info"]["sim_total"]} for rec in
					   full_recommendations["recommendations"]]
	return recommendations


@app.post("/v1/recommend/",
		  summary="Get recommendations for a user profile (main endpoint)",
		  response_model=List[Recommendation],
		  tags=["v1"],
		  responses={
			  200: {
				  "description": "Recommendations for the userId",
				  "content": {
					  "application/json": {
						  "example": [
							  {"title": "Article 1", "recommendation_value": 0.5},
							  {"title": "Article 2", "recommendation_value": 0.3},
							  {"title": "Article 3", "recommendation_value": 0.1},
						  ]
					  }
				  }
			  },
		  })
async def recommendV1(item: UserProfileSchema, response: Response):
	# TODO: implement 0 result handling
	user_profile = item.model_dump()

	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	full_recommendations = get_recommendations(user_profile)
	recommendations = [{"title": rec["title"], "recommendation_value": rec["info"]["sim_total"]} for rec in
					   full_recommendations["recommendations"]]
	return recommendations


@app.get("/v2/debug_recommend/{userId}",
		 summary="Get recommendations for a userId with debug information",
		 response_model=DebugResponse,
		 tags=["v2"],
		 responses={
			 200: {
				 "description": "Recommendations for the userId",
				 "content": {
					 "application/json": {
						 "example": {
							 "recommendations": [
								 {
									 "title": "Staying active to lower your risk of breast cancer: A simple guide to WHO’s physical activity recommendations",
									 "info": {
										 "sim_total": 0.875,
										 "goals": [
											 "increase_physical_activity",
											 "improve_mental_health"
										 ]
									 }
								 },
								 {
									 "title": "Staying active to lower your risk of breast cancer: A simple guide to greek physical activity recommendations",
									 "info": {
										 "sim_total": 0.875,
										 "goals": [
											 "increase_physical_activity",
											 "improve_mental_health"
										 ]
									 }
								 },
								 {
									 "title": "News_Article_About_Diet_And_Exercise",
									 "info": {
										 "sim_total": 0.75,
										 "goals": [
											 "improve_diet_quality",
											 "increase_physical_activity"
										 ]
									 }
								 },
								 {
									 "title": "Youtube_Video_About_Improving_Life_Quality",
									 "info": {
										 "sim_total": 0.75,
										 "goals": [
											 "cease_smoking",
											 "reduce_alcohol_consumption",
											 "improve_diet_quality",
											 "increase_physical_activity",
											 "improve_mental_health"
										 ]
									 }
								 },
								 {
									 "title": "9 Proven Benefits of Physical Activity",
									 "info": {
										 "sim_total": 0.75,
										 "goals": [
											 "increase_physical_activity"
										 ]
									 }
								 },
								 {
									 "title": "Staying active with breast cancer: Simple tips to keep you moving",
									 "info": {
										 "sim_total": 0.75,
										 "goals": [
											 "increase_physical_activity"
										 ]
									 }
								 },
								 {
									 "title": "Tips for a more active lifestyle",
									 "info": {
										 "sim_total": 0.75,
										 "goals": [
											 "increase_physical_activity",
											 "improve_mental_health"
										 ]
									 }
								 },
								 {
									 "title": "Do I need to walk 10,000 steps per day?",
									 "info": {
										 "sim_total": 0.5,
										 "goals": [
											 "increase_physical_activity"
										 ]
									 }
								 },
								 {
									 "title": "What are the different types of physical activity?",
									 "info": {
										 "sim_total": 0.5,
										 "goals": [
											 "increase_physical_activity"
										 ]
									 }
								 }
							 ],
							 "user_profile": {
								 "increase_physical_activity": {
									 "str": 0.75,
									 "ttm_stages": 4
								 },
								 "improve_diet_quality": {
									 "str": 0.25,
									 "ttm_stages": 4
								 },
								 "reduce_alcohol_consumption": {
									 "str": 0.25,
									 "ttm_stages": 4
								 },
								 "cease_smoking": {
									 "str": 0.0,
									 "ttm_stages": 4
								 },
								 "improve_mental_health": {
									 "str": 0.25,
									 "ttm_stages": 4
								 },
								 "seek_medical_help": {
									 "str": 0.25,
									 "ttm_stages": 4
								 }
							 },
							 "diffs": {
								 "integrated": {
									 "general_health": 4,
									 "quality_of_life": 5,
									 "user_status": "survivor",
									 "mental_health": 4,
									 "alcohol_consumption": 4,
									 "eating_pyramid_score": 5,
									 "usage_of_tobacco_products": 5,
									 "vigorous_activity": 1,
									 "moderate_activity": 3,
									 "walking": 1,
									 "sitting": 3,
									 "physical_activity_level": 2,
									 "proximity_to_exercise_facilities": 2,
									 "limitation_to_increase_physical_activity": 2,
									 "enhancing_factors_to_increase_physical_activity": 3,
									 "limitation_to_improve_diet_quality": 3,
									 "enhancing_factors_to_improve_diet_quality": 2,
									 "level_of_symptoms": 3
								 },
								 "aggregated": {
									 "increase_physical_activity": 4,
									 "improve_diet_quality": 2,
									 "reduce_alcohol_consumption": 2,
									 "cease_smoking": 1,
									 "improve_mental_health": 2,
									 "seek_medical_help": 2
								 },
								 "ttm": {
									 "increase_physical_activity": {
										 "str": 4,
										 "ttm_stages": 4
									 },
									 "improve_diet_quality": {
										 "str": 2,
										 "ttm_stages": 4
									 },
									 "reduce_alcohol_consumption": {
										 "str": 2,
										 "ttm_stages": 4
									 },
									 "cease_smoking": {
										 "str": 1,
										 "ttm_stages": 4
									 },
									 "improve_mental_health": {
										 "str": 2,
										 "ttm_stages": 4
									 },
									 "seek_medical_help": {
										 "str": 2,
										 "ttm_stages": 4
									 }
								 }
							 }
						 }
					 }
				 }
			 },
			 500: {
				 "description": "Internal server error",
				 "content": {
					 "application/json": {
						 "example": {
							 "error": "There was an error retrieving the user profile"
						 }
					 }
				 }
			 }
		 })
async def debug_recommend(userId: str, response: Response):
	# TODO: implement 0 result handling
	user_profile = create_user_profile(userId)

	# TODO: handle missing userId and Database-connection errors differently
	if not user_profile:
		response.status_code = 500
		return {"error": "There was an error retrieving the user profile"}

	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	return get_recommendations(user_profile)


@app.post("/v1/debug_recommend",
		  summary="Get recommendations for a user profile with debug information",
		  response_model=DebugResponse,
		  tags=["v1"],
		  responses={
			  200: {
				  "description": "Recommendations for the userId",
				  "content": {
					  "application/json": {
						  "example": {
							  "recommendations": [
								  {
									  "title": "Staying active to lower your risk of breast cancer: A simple guide to WHO’s physical activity recommendations",
									  "info": {
										  "sim_total": 0.875,
										  "goals": [
											  "increase_physical_activity",
											  "improve_mental_health"
										  ]
									  }
								  },
								  {
									  "title": "Staying active to lower your risk of breast cancer: A simple guide to greek physical activity recommendations",
									  "info": {
										  "sim_total": 0.875,
										  "goals": [
											  "increase_physical_activity",
											  "improve_mental_health"
										  ]
									  }
								  },
								  {
									  "title": "News_Article_About_Diet_And_Exercise",
									  "info": {
										  "sim_total": 0.75,
										  "goals": [
											  "improve_diet_quality",
											  "increase_physical_activity"
										  ]
									  }
								  },
								  {
									  "title": "Youtube_Video_About_Improving_Life_Quality",
									  "info": {
										  "sim_total": 0.75,
										  "goals": [
											  "cease_smoking",
											  "reduce_alcohol_consumption",
											  "improve_diet_quality",
											  "increase_physical_activity",
											  "improve_mental_health"
										  ]
									  }
								  },
								  {
									  "title": "9 Proven Benefits of Physical Activity",
									  "info": {
										  "sim_total": 0.75,
										  "goals": [
											  "increase_physical_activity"
										  ]
									  }
								  },
								  {
									  "title": "Staying active with breast cancer: Simple tips to keep you moving",
									  "info": {
										  "sim_total": 0.75,
										  "goals": [
											  "increase_physical_activity"
										  ]
									  }
								  },
								  {
									  "title": "Tips for a more active lifestyle",
									  "info": {
										  "sim_total": 0.75,
										  "goals": [
											  "increase_physical_activity",
											  "improve_mental_health"
										  ]
									  }
								  },
								  {
									  "title": "Do I need to walk 10,000 steps per day?",
									  "info": {
										  "sim_total": 0.5,
										  "goals": [
											  "increase_physical_activity"
										  ]
									  }
								  },
								  {
									  "title": "What are the different types of physical activity?",
									  "info": {
										  "sim_total": 0.5,
										  "goals": [
											  "increase_physical_activity"
										  ]
									  }
								  }
							  ],
							  "user_profile": {
								  "increase_physical_activity": {
									  "str": 0.75,
									  "ttm_stages": 4
								  },
								  "improve_diet_quality": {
									  "str": 0.25,
									  "ttm_stages": 4
								  },
								  "reduce_alcohol_consumption": {
									  "str": 0.25,
									  "ttm_stages": 4
								  },
								  "cease_smoking": {
									  "str": 0.0,
									  "ttm_stages": 4
								  },
								  "improve_mental_health": {
									  "str": 0.25,
									  "ttm_stages": 4
								  },
								  "seek_medical_help": {
									  "str": 0.25,
									  "ttm_stages": 4
								  }
							  },
							  "diffs": {
								  "integrated": {
									  "general_health": 4,
									  "quality_of_life": 5,
									  "user_status": "survivor",
									  "mental_health": 4,
									  "alcohol_consumption": 4,
									  "eating_pyramid_score": 5,
									  "usage_of_tobacco_products": 5,
									  "vigorous_activity": 1,
									  "moderate_activity": 3,
									  "walking": 1,
									  "sitting": 3,
									  "physical_activity_level": 2,
									  "proximity_to_exercise_facilities": 2,
									  "limitation_to_increase_physical_activity": 2,
									  "enhancing_factors_to_increase_physical_activity": 3,
									  "limitation_to_improve_diet_quality": 3,
									  "enhancing_factors_to_improve_diet_quality": 2,
									  "level_of_symptoms": 3
								  },
								  "aggregated": {
									  "increase_physical_activity": 4,
									  "improve_diet_quality": 2,
									  "reduce_alcohol_consumption": 2,
									  "cease_smoking": 1,
									  "improve_mental_health": 2,
									  "seek_medical_help": 2
								  },
								  "ttm": {
									  "increase_physical_activity": {
										  "str": 4,
										  "ttm_stages": 4
									  },
									  "improve_diet_quality": {
										  "str": 2,
										  "ttm_stages": 4
									  },
									  "reduce_alcohol_consumption": {
										  "str": 2,
										  "ttm_stages": 4
									  },
									  "cease_smoking": {
										  "str": 1,
										  "ttm_stages": 4
									  },
									  "improve_mental_health": {
										  "str": 2,
										  "ttm_stages": 4
									  },
									  "seek_medical_help": {
										  "str": 2,
										  "ttm_stages": 4
									  }
								  }
							  }
						  }
					  }
				  }
			  },
		  })
async def debug_recommend(item: UserProfileSchema, response: Response):
	# TODO: implement 0 result handling
	user_profile = item.model_dump()

	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	return get_recommendations(user_profile)


@app.post("/mini_course",
		  summary="",
		  include_in_schema=False,
		  responses={
			  200: {
				  "description": "Recommendations for the userId",
				  "content": {
					  "application/json": {
						  "example": {
						  }
					  }
				  }
			  }
		  })
async def mini_course(item: Request, index: int = 0):
	obj = await item.json()
	mini_course_obj = obj["mini_course"]
	user_profile = obj["user_profile"]
	print(f"Index: {index}")
	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	print(f"Mini Course: {json5.dumps(mini_course_obj, indent=4, quote_keys=True)}")
	if index < 0 or index >= len(mini_course_obj["goals"]):
		return {"error": "Index out of bounds"}

	mini_course_objective = mini_course_obj["goals"][index]["objective"]
	recommendations = get_recommendations(user_profile)["recommendations"]
	filtered_recommendations = filter_recommendations(recommendations, mini_course_objective)
	print(f"Filtered Recommendations: {json5.dumps(filtered_recommendations, indent=4, quote_keys=True)}")
	return filtered_recommendations


@app.get("/{userId}/day",
		 summary="Get the active mini course day for a user",
		 response_model=DayResponse,
		 tags=["helper"],
		 responses={
			 200: {
				 "description": "The active mini course day for the user",
				 "content": {
					 "application/json": {
						 "example": {
							 "day": 1
						 }
					 }
				 }
			 },
			 500: {
				 "description": "Internal server error",
				 "content": {
					 "application/json": {
						 "example": {
							 "error": "There was an error retrieving the user profile"
						 }
					 }
				 }
			 },
			 400: {
				 "description": "User ID must be an integer",
				 "content": {
					 "application/json": {
						 "example": {
							 "error": "User ID must be an integer"
						 }
					 }
				 }}
		 })
async def get_day(userId: str, response: Response):
	print(f"User ID: {userId}")
	try:
		userId = int(userId)
	except ValueError:
		response.status_code = 400
		return {"error": "User ID must be an integer"}

	# TODO: get the user from the database
	return get_day_by_user_id(userId)


@app.get("/mini_course/{miniCourseId}/{day}",
		 summary="Get the schedule and educational material for a corresponding mini course day",
		 response_model=MiniCourseScheduleAndEducationalMaterialsResponse,
		 tags=["mini-course"],
		 responses={
			 200: {
				 "description": "The schedule and educational material for the mini course with id `123` and day `4`",
				 "content": {
					 "application/json": {
						 "example": {
							 "schedule": {
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
							 },
							 "educational_material": [
								 "64d29f7e92cb40a5c4567d12"
							 ]
						 }
					 }
				 }
			 },
			 400: {
				 "description": "Malformed request",
				 "content": {
					 "application/json": {
						 "example": {
							 "error": "Day must be an integer"
						 }
					 }
				 }
			 },
			 404: {
				 "description": "Mini course not found",
				 "content": {
					 "application/json": {
						 "example": {
							 "error": "Mini course not found"
						 }
					 }
				 }
			 }
		 })
async def get_mini_course_day(miniCourseId: str, day: str, response: Response):
	print(f"Mini Course ID: {miniCourseId}")
	print(f"Day: {day}")
	try:
		day = int(day)
	except ValueError:
		response.status_code = 400
		return {"error": "Day must be an integer"}

	if miniCourseId not in mini_course_library:
		response.status_code = 404
		return {"error": "Mini course not found"}

	mini_course = mini_course_library[miniCourseId]

	all_educational_material = [mini_course["educational_materials"][i][day] for i in
								range(len(mini_course["educational_materials"]))]

	final_educational_material = []
	for list_ in all_educational_material:
		for item in list_:
			final_educational_material.append(item)

	schedule = None
	for s in mini_course["default_schedule"]:
		if s["day"] == day:
			schedule = s

	if not schedule:
		response.status_code = 404
		return {"error": "Day not in default schedule"}
	return {
		"schedule": schedule,
		"educational_material": final_educational_material
	}


@app.get("/v1/physical_activity_level",
		 summary="Get the physical activity level for a user profile",
		 response_model=int,
		 tags=["v1"],
		 responses={
			 200: {
				 "description": "The physical activity level for the user profile",
				 "content": {
					 "application/json": {
						 "example": 2
					 }
				 }
			 }
		 })
async def get_physical_activity_levelV1(item: UserProfileSchema):
	user_profile = item.model_dump()
	return get_physical_activity_level(user_profile)


@app.get("/v2/physical_activity_level/{userId}",
		 summary="Get the physical activity level for a userId",
		 tags=["v2"],
		 responses={
			 200: {
				 "description": "The physical activity level for the user profile",
				 "content": {
					 "application/json": {
						 "example": 2
					 }
				 }
			 }
		 }
		 )
async def get_physical_activity_levelV2(userId: str, response: Response):
	print(f"User ID: {userId}")
	questions = ["vigorous_activity_days",
				 "vigorous_activity_duration",
				 "moderate_activity_days",
				 "moderate_activity_duration",
				 "walking_days_10_min",
				 "walking_duration",
				 "sitting_time_weekday",
				 "activity_days_10_min",
				 "leisure_activity_duration",
				 "steps_per_day"]
	user_profile = create_user_profile(userId, questions)

	if len(user_profile.keys()) == 3:
		raise HTTPException(status_code=404,
							detail="User not found or user hasn't answered any physical activity question")
	return get_physical_activity_level(user_profile)


@app.get("/tip_recommend/{PA_level}")
async def recommend_tip(PA_level: int):
	print(f"PA Level: {PA_level}")
	if PA_level <= 2:
		return {"tips": get_random_tips("beginner")}
	elif PA_level <= 4:
		return {"tips": get_random_tips("intermediate")}
	else:
		return {"tips": get_random_tips("advanced")}


# Only for debugging
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)