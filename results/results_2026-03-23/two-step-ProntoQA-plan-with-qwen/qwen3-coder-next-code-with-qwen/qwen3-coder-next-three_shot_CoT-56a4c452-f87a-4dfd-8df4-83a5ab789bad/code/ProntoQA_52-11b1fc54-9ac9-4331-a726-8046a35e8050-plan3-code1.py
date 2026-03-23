# Import required modules
from pyke import knowledge_engine

# Create and initialize the knowledge engine
engine = knowledge_engine.engine(__file__)
engine.activate('rules')

# Facts:
Facts:
facts.is_a("Polly", "jompus", True)

# Rules:
Rules:
foreach
    facts.is_a($x, "jompus", True)
assert
    facts.is_a($x, "dumpus", True)

foreach
    facts.is_a($x, "dumpus", True)
assert
    facts.is_a($x, "zumpus", True)

foreach
    facts.is_a($x, "zumpus", True)
assert
    facts.is_a($x, "wumpus", True)

foreach
    facts.is_a($x, "wumpus", True)
assert
    facts.is_a($x, "impus", True)

foreach
    facts.is_a($x, "impus", True)
assert
    facts.is_a($x, "tumpus", True)

foreach
    facts.is_a($x, "impus", True)
assert
    facts.blue($x, True)

foreach
    facts.is_a($x, "tumpus", True)
assert
    facts.is_a($x, "numpus", True)

# Query:
Query:
facts.blue("Polly", True)