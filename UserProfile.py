from ExtraDataClasses import CancerData, MedConditionData


class UserProfile:
    def __init__(self, age: int, ethnicity: str, economic_level: int, social_level: int, education_level: int,
                 height_meters: float, weight_kg: float, alcohol_consumption: int, smoking: int, eating_habits: int,
                 physical_activity: int, status: CancerData = None, medical_conditions: list[MedConditionData] = None,
                 mental_conditions: list[MedConditionData] = None):
        self.age = age
        self.ethnicity = ethnicity
        self.economic_level = economic_level
        self.social_level = social_level
        self.education_level = education_level
        self.height_meters = height_meters
        self.weight_kg = weight_kg
        self.status = status
        self.medical_conditions = medical_conditions
        self.mental_conditions = mental_conditions
        self.alcohol_consumption = alcohol_consumption
        self.smoking = smoking
        self.eating_habits = eating_habits
        self.physical_activity = physical_activity