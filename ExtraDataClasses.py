class CancerData:
    def __init__(self, active: bool, cancer_duration_days: int, therapy_type: str, last_treatment_date: str):
        self.active = active
        self.cancer_duration_days = cancer_duration_days
        self.therapy_type = therapy_type
        self.last_treatment_date = last_treatment_date


class MedConditionData:
    def __init__(self, medical_condition: str):
        self.medical_condition = medical_condition