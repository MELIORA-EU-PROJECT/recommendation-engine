from enum import Enum, auto
from typing import Dict

from Rules_Config import Rules


# ! DON'T CHANGE THIS CLASS
class Goal_State:
    counter = 0

    def __init__(self, title: str,
                 rules,
                 negations: list[Rules] = None):
        """

        :param title: The title of the goal state, e.g. "Increase Physical Activity"
        :param rules: (list[Rules] | list[list[Rules]] | (Goal_State, list[Rules]) | (Goal_State, list[list[Rules]]) )!!THIS WAS THE TYPE ANNOTATION BUT PYTHON DOESN'T LIKE IT!!. A list of rules that must be met for the goal to be achieved. This can be either a list of rules, if our goal can be described by a single set of rules. Or multiple lists of rules, if multiple sets of rules can describe the goal. Or a tuple of another goal state and the aforementioned options, if our goal can be described as an extension of another goal.
        :param negations: (Optional) A list of rules that must NOT be met for the goal to be achieved. e.g. If the goal is to increase meat consumption, we might want to make sure the user is not a vegetarian.
        """
        self.title = title
        self.rules = rules
        self.negations = negations
        Goal_State.counter += 1

    def __call__(self, rules_met: Dict[Rules, bool]) -> bool:
        """
        Checks if all rules are met for the goal to be achieved (and all negations are NOT met).
        :param rules_met: A dictionary that maps each rule to a boolean value, indicating whether the rule is met or not.
        :return: True if the goal is achieved, False otherwise.
        """

        # If rules is multiple lists of rules
        if isinstance(self.rules[0], list):
            # True if all rules are met
            all_rules_met = any(all(rules_met[rule] for rule in rule_group) for rule_group in self.rules)

        # If rules is an extension of another goal
        elif isinstance(self.rules[0], Goals):

            # If the extension has multiple rule groups
            if isinstance(self.rules[1][0], list):
                all_rules_met = any(all(rules_met[rule] for rule in rule_group) for rule_group in self.rules[1])
            # If the extension has a single rule list
            else:
                all_rules_met = all(rules_met[rule] for rule in self.rules[1])

            rules_of_extended_goal = goal_states[self.rules[0]]
            all_rules_met = rules_of_extended_goal(rules_met) and all_rules_met

        # If rules is a single list of rules
        else:
            all_rules_met = all(rules_met[rule] for rule in self.rules)

        if self.negations:
            # True if all negations are NOT met
            all_negations_met = all(not rules_met[rule] for rule in self.negations)
            return all_rules_met and all_negations_met

        return all_rules_met


# ! DON'T CHANGE THIS CLASS

class Goals(Enum):
    INCREASE_PHYSICAL_ACTIVITY = 0
    DECREASE_ALCOHOL_CONSUMPTION = auto()
    CHANGE_EATING_HABITS = auto()
    INCREASE_MEAT_CONSUMPTION = auto()

    def __repr__(self):
        default = super().__repr__()
        res = default.split(".")[1].split(":")[0]
        return f"{res}"


goal_states: Dict[Goals, Goal_State] = {
    Goals.INCREASE_PHYSICAL_ACTIVITY: Goal_State("Increase Physical Activity",
                                                 [Rules.BMI_GREATER_THAN_25, Rules.LOW_PHYSICAL_ACTIVITY]),
    Goals.DECREASE_ALCOHOL_CONSUMPTION: Goal_State("Decrease Alcohol Consumption", [Rules.HIGH_ALCOHOL_CONSUMPTION]),
    Goals.CHANGE_EATING_HABITS: Goal_State("Change Eating Habits", [Rules.BMI_GREATER_THAN_25]),
    Goals.INCREASE_MEAT_CONSUMPTION: Goal_State("Increase Meat Consumption",
                                                (Goals.CHANGE_EATING_HABITS, [Rules.HAS_MEDICAL_CONDITIONS]),
                                                [Rules.IS_VEGAN]),
}

assert len(
    goal_states) == len(
    Goals), f"Number of goals does not match the number of goals defined. Expected {len(Goals)} goals, got {len(goal_states)} goals."