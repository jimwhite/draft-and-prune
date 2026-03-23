# PyKe program for the zumpus logic puzzle

from pyke import knowledge_engine

# Create knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts section
Facts:
    is_a('Stella', 'numpus', True)

# Rules section
Rules:
    # Every zumpus is metallic
    foreach is_a($thing, 'zumpus', True)
        assert is_metallic($thing, True)

    # Each zumpus is a wumpus
    foreach is_a($thing, 'zumpus', True)
        assert is_a($thing, 'wumpus', True)

    # Wumpuses are not floral
    foreach is_a($thing, 'wumpus', True)
        assert is_floral($thing, False)

    # Every wumpus is a numpus
    foreach is_a($thing, 'wumpus', True)
        assert is_a($thing, 'numpus', True)

    # Numpuses are happy
    foreach is_a($thing, 'numpus', True)
        assert is_happy($thing, True)

    # Each numpus is an impus
    foreach is_a($thing, 'numpus', True)
        assert is_a($thing, 'impus', True)

    # Impuses are kind
    foreach is_a($thing, 'impus', True)
        assert is_kind($thing, True)

    # Every impus is a rompus
    foreach is_a($thing, 'impus', True)
        assert is_a($thing, 'rompus', True)

    # Every rompus is large
    foreach is_a($thing, 'rompus', True)
        assert is_large($thing, True)

    # Vumpuses are opaque
    foreach is_a($thing, 'vumpus', True)
        assert is_opaque($thing, True)

    # Every rompus is a jompus
    foreach is_a($thing, 'rompus', True)
        assert is_a($thing, 'jompus', True)

    # Each jompus is cold
    foreach is_a($thing, 'jompus', True)
        assert is_cold($thing, True)

    # Jompuses are dumpuses
    foreach is_a($thing, 'jompus', True)
        assert is_a($thing, 'dumpus', True)

    # Each dumpus is not opaque
    foreach is_a($thing, 'dumpus', True)
        assert is_opaque($thing, False)

    # Dumpuses are yumpuses
    foreach is_a($thing, 'dumpus', True)
        assert is_a($thing, 'yumpus', True)

    # Yumpuses are spicy
    foreach is_a($thing, 'yumpus', True)
        assert is_spicy($thing, True)

    # Each yumpus is a tumpus
    foreach is_a($thing, 'yumpus', True)
        assert is_a($thing, 'tumpus', True)

# Query section
Query:
    is_opaque('Stella', True)