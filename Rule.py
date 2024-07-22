from typing import Callable

from UserProfile import UserProfile


class Rule:
    counter = 0

    def __init__(self, title: str, predicate: Callable[[UserProfile], bool]):
        """
        :param title: The title of the goal state, e.g. "age > 50"
        :param predicate: A function that returns True if the rule is met, e.g. for the example title above we would have this parameter lambda user: user.age > 50
        """
        self.title = title
        self.predicate = predicate
        Rule.counter += 1

    def __call__(self, user: UserProfile) -> bool:
        return self.predicate(user)