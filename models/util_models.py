from pydantic import BaseModel
from typing import Literal, Dict

from models.recommendation import DebugRecommendation
from models.user_profile import DebugUserProfile


class TTMInfo(BaseModel):
	str: int
	ttm_stages: int


class AggregatedData(BaseModel):
	increase_physical_activity: int
	improve_diet_quality: int
	reduce_alcohol_consumption: int
	cease_smoking: int
	improve_mental_health: int
	seek_medical_help: int


class IntegratedData(BaseModel):
	general_health: int
	quality_of_life: int
	user_status: str
	mental_health: int
	alcohol_consumption: int
	eating_pyramid_score: int
	usage_of_tobacco_products: int
	vigorous_activity: int
	moderate_activity: int
	walking: int
	sitting: int
	physical_activity_level: int
	proximity_to_exercise_facilities: int
	limitation_to_increase_physical_activity: int
	enhancing_factors_to_increase_physical_activity: int
	limitation_to_improve_diet_quality: int
	enhancing_factors_to_improve_diet_quality: int
	level_of_symptoms: int


class TTMData(BaseModel):
	increase_physical_activity: TTMInfo
	improve_diet_quality: TTMInfo
	reduce_alcohol_consumption: TTMInfo
	cease_smoking: TTMInfo
	improve_mental_health: TTMInfo
	seek_medical_help: TTMInfo


class DiffsData(BaseModel):
	integrated: IntegratedData
	aggregated: AggregatedData
	ttm: TTMData


class DebugResponse(BaseModel):
	recommendations: list[DebugRecommendation]
	user_profile: DebugUserProfile
	diffs: DiffsData

class DayResponse(BaseModel):
	day: int