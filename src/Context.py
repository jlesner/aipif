from collections import defaultdict

class Context:
    """
        A class to hold "context" which replaces use of global variables.

        Attributes:

            config: dict
                A dictionary that holds configuration options.
                Only strings are allowed as keys and values.

            state: dict
                Function lookup table built by configure() from context.config.
                Also holds state shared between functions.
                See aipif.state_setup() for details.

            stats: defaultdict(int)
                A dictionary used to collect run-time statistics.
    """

    def __init__(self, config=dict(), state=dict(), stats=defaultdict(int)):
        self.config = config
        self.state = state
        self.stats = stats

    def __repr__(self):
        return f"config:{self.config}\nstats:{self.stats}\nstate:{self.state}"


