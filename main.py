"""
Copyright © 2024 Nikos Gournakis
All rights reserved
"""
from typing import Dict

import Goals_Config
import Rules_Config
from ExtraDataClasses import CancerData, MedConditionData
from Rules_Config import Rules
from Goals_Config import Goals
from UserProfile import UserProfile

# All the users, this will later be a database query
user_profiles = [
    UserProfile(60, "White", 3, 3, 3, 1.75, 80, 3, 3, 3, 3, False,
                CancerData(True, 60, "Chemotherapy", "2021-01-01"), [MedConditionData("low blood pressure")]), ]

# For now, we will just use the first user
user_profile = user_profiles[0]


def rules_met(user_profile: UserProfile) -> Dict[Rules, bool]:
    """
    Returns a dictionary of rules and whether they are met or not

    :param user_profile: The user profile to check the rules against
    :return: A dictionary of rules and whether they are met or not
    """
    rules_met: Dict[Rules, bool] = {rule_id: predicate(user_profile) for rule_id, predicate in
                                    Rules_Config.rules.items()}
    return rules_met


def goals_met(rules_met: Dict[Rules, bool]) -> Dict[Goals, bool]:
    """
    Returns a dictionary of goals and whether they are met or not
    :param rules_met: The rules that are met to check the goals against
    :return: A dictionary of goals and whether they are met or not
    """
    goals_met = {goal: goal_state(rules_met) for goal, goal_state in Goals_Config.goal_states.items()}
    return goals_met


print(rules_met(user_profile))
print(goals_met(rules_met(user_profile)))

# CONFLICT RESOLUTION WIP