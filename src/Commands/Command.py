from typing import Callable, List


class Command:
    def __init__(self, command: Callable[[List[str]], bool | None], requirements: List[str] = None):
        self.command = command
        self.requirements = requirements
        self.executions = 0

    def __call__(self, *args, **kwargs):
        return_value = self.command(*args, **kwargs)
        if return_value is not False:
            self.executions += 1
        return return_value
