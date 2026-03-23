# Import required modules
from pyke import knowledge_engine

# Create and initialize the knowledge engine
engine = knowledge_engine.engine(__file__)
engine.activate('rules')

# Facts section
Facts:
    is_a(Polly, jompus, True)

# Rules section
Rules:
    # Every jompus is spicy.
    foreach facts.is_a($thing, jompus, True)
        assert facts.is_spicy($thing, True)

    # Every jompus is a dumpus.
    foreach facts.is_a($thing, jompus, True)
        assert facts.is_a($thing, dumpus, True)

    # Each dumpus is not transparent.
    foreach facts.is_a($thing, dumpus, True)
        assert facts.is_transparent($thing, False)

    # Each dumpus is a zumpus.
    foreach facts.is_a($thing, dumpus, True)
        assert facts.is_a($thing, zumpus, True)

    # Zumpuses are feisty.
    foreach facts.is_a($thing, zumpus, True)
        assert facts.is_feisty($thing, True)

    # Zumpuses are wumpuses.
    foreach facts.is_a($thing, zumpus, True)
        assert facts.is_a($thing, wumpus, True)

    # Each wumpus is not dull.
    foreach facts.is_a($thing, wumpus, True)
        assert facts.is_dull($thing, False)

    # Every wumpus is an impus.
    foreach facts.is_a($thing, wumpus, True)
        assert facts.is_a($thing, impus, True)

    # Every vumpus is not blue.
    foreach facts.is_a($thing, vumpus, True)
        assert facts.is_blue($thing, False)

    # Impuses are blue.
    foreach facts.is_a($thing, impus, True)
        assert facts.is_blue($thing, True)

    # Impuses are tumpuses.
    foreach facts.is_a($thing, impus, True)
        assert facts.is_a($thing, tumpus, True)

    # Tumpuses are not floral.
    foreach facts.is_a($thing, tumpus, True)
        assert facts.is_floral($thing, False)

    # Each tumpus is a numpus.
    foreach facts.is_a($thing, tumpus, True)
        assert facts.is_a($thing, numpus, True)

# Query section
Query:
    is_blue(Polly, True)