# Rule based system Prototype

## Author : Nikos Gournakis

## Quick Start

`python main.py`

## Description
This is a very simple prototype of my approach to a rule based system.
The system is based on a set of rules that are defined in the `Rules_Config.py` file.
To define a new rule you need to add the name in the `Rules enum` and then add the implementations
of the rule in the rules dictionary, where the key is the name that you just inserted in the enum and the
value is a `Rule` object. Each rule object is a simple predicate. Calling the `Rule` object will apply the rule
to the given `UserProfile`.

The second part of the system are the goal states defined in the `Goals_Config.py` file.
To define a new goal you need to add the name in the `Goals enum` and then add the implementations
of the goal in the `goal_states` dictionary, where the key is the name that you just inserted in the enum and the
value is a `Goal` object. Each goal can have rules and negation rules that define the achieving of the Goal.
Also, the `Goal` object can extend the rules of another goal by using passing the enum value of the goal that you want to extend
and the extending rules as a tuple for the rules param. Also, a `Goal` can have multiple sets of rules that can be used to achieve the goal,
this can be done by passing a list of lists of rules in the rules param.
Calling the `Goal` object will apply the rules and negation rules to the given `UserProfile` and return if the goal is achieved or not.