from collections import defaultdict

from click import Context

class ContextAware:
    """
    Base class for objects created with a Context

    Arguments:
        context:Context
            replaces global variables for tracking config / state / stats

    """
    def __init__(self, context:Context):
        self._context = context