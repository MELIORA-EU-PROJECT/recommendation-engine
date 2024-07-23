# This file is used to define the rules that will be used in the system.

from enum import Enum, auto
from Rule import Rule

class Rules(Enum):
    AGE_GREATER_THAN_50 = 0
    HAS_CANCER = auto()
    ETHNICITY_IS_WHITE = auto()
    ECONOMIC_LEVEL_IS_3 = auto()
    HAS_MEDICAL_CONDITIONS = auto()
    HAS_MENTAL_CONDITIONS = auto()
    BMI_GREATER_THAN_25 = auto()
    HIGH_ALCOHOL_CONSUMPTION = auto()
    IS_VEGAN = auto()
    LOW_PHYSICAL_ACTIVITY = auto()

    def __repr__(self):
        default = super().__repr__()
        res = default.split(".")[1].split(":")[0]
        return f"{res}"


rules = {
    Rules.AGE_GREATER_THAN_50: Rule("age > 50", lambda user: user.age > 50),
    Rules.HAS_CANCER: Rule("has Cancer", lambda user: user.status is not None and user.status.active),
    Rules.ETHNICITY_IS_WHITE: Rule("ethnicity is White", lambda user: user.ethnicity == "White"),
    Rules.ECONOMIC_LEVEL_IS_3: Rule("economic level is 3", lambda user: user.economic_level == 3),
    Rules.HAS_MEDICAL_CONDITIONS: Rule("has medical conditions",
                                       lambda user: user.medical_conditions is not None and len(
                                           user.medical_conditions) > 0),
    Rules.HAS_MENTAL_CONDITIONS: Rule("has mental conditions", lambda user: user.mental_conditions is not None and len(
        user.mental_conditions) > 0),
    Rules.BMI_GREATER_THAN_25: Rule("BMI > 25", lambda user: user.weight_kg / (user.height_meters ** 2) > 25),
    Rules.HIGH_ALCOHOL_CONSUMPTION: Rule("high alcohol consumption", lambda user: user.alcohol_consumption > 3),
    Rules.IS_VEGAN: Rule("is vegan", lambda user: user.is_vegan),
    Rules.LOW_PHYSICAL_ACTIVITY: Rule("low physical activity", lambda user: user.physical_activity < 3),

}
assert len(Rules) == len(
    rules), f"You might have forgotten to add a rule in the rules dictionary. You have defined {len(Rules)} rules, but you have {len(rules)} rules in the dictionary."

assert len(
    Rules) == Rule.counter, f"Number of rules defined does not match the number of rules implemented. You have defined {len(Rules)} rules, but you have implemented {Rule.counter} rules."