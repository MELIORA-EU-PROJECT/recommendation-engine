from pydantic import BaseModel


class Recommendation(BaseModel):
	title: str
	recommendation_value: float


class DebugRecommendationInfo(BaseModel):
	sim_total: float
	goals: list[str]


class DebugRecommendation(BaseModel):
	title: str
	info: DebugRecommendationInfo