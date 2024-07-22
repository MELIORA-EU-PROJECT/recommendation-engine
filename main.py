from typing import Dict

import Goals_Config
import Rules_Config
from ExtraDataClasses import CancerData, MedConditionData
from Rules_Config import Rules
from Goals_Config import Goals
from UserProfile import UserProfile

user_profiles = [
    UserProfile(60, "White", 3, 3, 3, 1.75, 80, 3, 3, 3, 3, False,
                CancerData(True, 60, "Chemotherapy", "2021-01-01"), [MedConditionData("low blood pressure")]), ]

user_profile = user_profiles[0]


def rules_met(user_profile: UserProfile) -> Dict[Rules, bool]:
    rules_met: Dict[Rules, bool] = {rule_id: predicate(user_profile) for rule_id, predicate in
                                    Rules_Config.rules.items()}
    return rules_met


def goals_met(rules_met: Dict[Rules, bool]) -> Dict[Goals, bool]:
    goals_met = {goal: goal_state(rules_met) for goal, goal_state in Goals_Config.goal_states.items()}
    return goals_met


print(rules_met(user_profile))
print(goals_met(rules_met(user_profile)))