from collections import defaultdict

from common.Context import Context

class ContextAware:
    """
    Base class for objects created with a Context

    Arguments:
        context:Context
            replaces global variables for tracking config / state / stats

    """
    def __init__(self, context:Context=Context()):
        self._context = context