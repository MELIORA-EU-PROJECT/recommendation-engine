"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""

import json5
import uvicorn

from utils import *

from fastapi import FastAPI, Request, Response

from colorama import init as colorama_init
from colorama import Fore, Style

colorama_init()

app = FastAPI()


@app.get("/",
		 summary="A simple health check endpoint",
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


@app.get("/recommend/{userId}",
		 summary="Get recommendations for a user profile (main endpoint)",
		 responses={
			 200: {
				 "description": "Recommendations for the user profile given",
				 "content": {
					 "application/json": {
						 "example": {
						 }
					 }
				 }
			 }
		 })
async def recommend(userId: str, response: Response):
	# TODO: implement 0 result handling
	user_profile = create_user_profile(userId)

	# TODO: handle missing userId and Database-connection errors differently
	if not user_profile:
		response.status_code = 500
		return {"error": "There was an error retrieving the user profile"}

	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	full_recommendations = get_recommendations(user_profile)
	recommendations = {k: v["sim_total"] for k, v in full_recommendations["recommendations"].items()}
	full_recommendations["recommendations"] = recommendations
	return full_recommendations


@app.get("/debug_recommend/{userId}", )
async def root(userId: str, response: Response):
	# TODO: implement 0 result handling
	user_profile = create_user_profile(userId)

	# TODO: handle missing userId and Database-connection errors differently
	if not user_profile:
		response.status_code = 500
		return {"error": "There was an error retrieving the user profile"}

	print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
	return get_recommendations(user_profile)


@app.post("/mini_course")
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


@app.get("/{user_id}/day")
async def get_day(user_id: str):
	try:
		user_id = int(user_id)
	except ValueError:
		return {"error": "User ID must be an integer"}
	return get_day_by_user_id(user_id)


@app.get("/mini_course/{mini_course_id}/{day}")
async def get_mini_course_day(mini_course_id: str, day: str):
	try:
		day = int(day)
	except ValueError:
		return {"error": "Day must be an integer"}

	if mini_course_id not in mini_course_library:
		return {"error": "Mini course not found"}

	mini_course = mini_course_library[mini_course_id]

	all_educational_material = [mini_course["educational_materials"][i][day] for i in
								range(len(mini_course["educational_materials"]))]

	final_educational_material = []
	for list_ in all_educational_material:
		for item in list_:
			final_educational_material.append(item)

	return {
		"schedule": mini_course["default_schedule"][day],
		"educational_material": final_educational_material
	}


# Only for debugging
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)