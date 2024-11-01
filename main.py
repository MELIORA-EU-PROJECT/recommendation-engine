"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""

import json5
import uvicorn

from utils import *

from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/debug_recommend")
async def root(item: Request):
    user_profile = await item.json()
    print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
    return get_recommendations(user_profile)


@app.post("/recommend")
async def recommend(item: Request):
    user_profile = await item.json()
    print(f"User Profile: {json5.dumps(user_profile, indent=4, quote_keys=True)}")
    full_recommendations = get_recommendations(user_profile)
    recommendations = {k: v["sim_total"] for k, v in full_recommendations["recommendations"].items()}
    full_recommendations["recommendations"] = recommendations
    return full_recommendations


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
    return mini_course_obj["goals"][index]


# Only for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)