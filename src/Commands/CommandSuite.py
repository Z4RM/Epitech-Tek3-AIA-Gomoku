from typing import Callable, List


class CommandSuite:
    def __init__(self, suite_iteration: Callable[[List[str]], bool | None], ender: str, suite_end: Callable[[List[str]], bool | None]):
        self.suite_iteration = suite_iteration
        self.ender = ender
        self.suite_end = suite_end
        self.initialized = False

    def __call__(self, *args, **kwargs):
        if not self.initialized:
            self.initialized = True
            return
        if args[0][0] == self.ender:
            self.initialized = False
            return self.suite_end(*args, **kwargs)
        return self.suite_iteration(*args, **kwargs)
