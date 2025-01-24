from typing import Literal

from pydantic import BaseModel


class ScheduleStep(BaseModel):
	time: str
	type: Literal["goal", "educational_material", "end_of_week_mini_quiz"]


class ScheduleData(BaseModel):
	day: int
	order: list[ScheduleStep]


class MiniCourseScheduleAndEducationalMaterialsResponse(BaseModel):
	schedule: ScheduleData
	educational_material: list[str]