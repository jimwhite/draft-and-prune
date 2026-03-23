# Import required modules
from pyke import knowledge_engine

# Create and initialize the knowledge engine
engine = knowledge_engine.engine(__file__)
engine.activate('rules')

# Facts section
Facts:
facts.is_a("Polly", "jompus", True)

# Rules section
Rules:
# Rule: Every jompus is spicy.
jompus_is_spicy
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_spicy($thing, True)

# Rule: Every jompus is a dumpus.
jompus_is_dumpus
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "dumpus", True)

# Rule: Each dumpus is not transparent.
dumpus_is_not_transparent
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_transparent($thing, False)

# Rule: Each dumpus is a zumpus.
dumpus_is_zumpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Zumpuses are feisty.
zumpus_is_feisty
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_feisty($thing, True)

# Rule: Zumpuses are wumpuses.
zumpus_is_wumpus
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Each wumpus is not dull.
wumpus_is_not_dull
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_dull($thing, False)

# Rule: Every wumpus is an impus.
wumpus_is_impus
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "impus", True)

# Rule: Every vumpus is not blue.
vumpus_is_not_blue
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_blue($thing, False)

# Rule: Impuses are blue.
impus_is_blue
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_blue($thing, True)

# Rule: Impuses are tumpuses.
impus_is_tumpus
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_a($thing, "tumpus", True)

# Rule: Tumpuses are not floral.
tumpus_is_not_floral
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_floral($thing, False)

# Rule: Each tumpus is a numpus.
tumpus_is_numpus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Query section
Query:
engine.assert_fact('facts', 'is_a', 'Polly', 'jompus', True)
engine.run()
result = engine.query('facts.is_blue("Polly", True)')
print(result)