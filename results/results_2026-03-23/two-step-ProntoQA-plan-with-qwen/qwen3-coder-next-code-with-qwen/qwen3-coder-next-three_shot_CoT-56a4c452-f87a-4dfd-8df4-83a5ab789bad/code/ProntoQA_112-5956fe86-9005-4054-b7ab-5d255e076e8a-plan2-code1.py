from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts
facts.is_a("Max", "numpus", True)

# Rules
# Rule: Each rompus is not large.
rule rompus_is_not_large:
    foreach facts.is_a($thing, "rompus", True)
    assert facts.is_large($thing, False)

# Rule: Every rompus is a numpus.
rule rompus_is_numpus:
    foreach facts.is_a($thing, "rompus", True)
    assert facts.is_a($thing, "numpus", True)

# Rule: Every numpus is fruity.
rule numpus_is_fruity:
    foreach facts.is_a($thing, "numpus", True)
    assert facts.is_fruity($thing, True)

# Rule: Numpuses are wumpuses.
rule numpus_is_wumpus:
    foreach facts.is_a($thing, "numpus", True)
    assert facts.is_a($thing, "wumpus", True)

# Rule: Wumpuses are not metallic.
rule wumpus_is_not_metallic:
    foreach facts.is_a($thing, "wumpus", True)
    assert facts.is_metallic($thing, False)

# Rule: Wumpuses are tumpuses.
rule wumpus_is_tumpus:
    foreach facts.is_a($thing, "wumpus", True)
    assert facts.is_a($thing, "tumpus", True)

# Rule: Tumpuses are cold.
rule tumpus_is_cold:
    foreach facts.is_a($thing, "tumpus", True)
    assert facts.is_cold($thing, True)

# Rule: Dumpuses are not brown.
rule dumpus_is_not_brown:
    foreach facts.is_a($thing, "dumpus", True)
    assert facts.is_brown($thing, False)

# Rule: Tumpuses are jompuses.
rule tumpus_is_jompus:
    foreach facts.is_a($thing, "tumpus", True)
    assert facts.is_a($thing, "jompus", True)

# Rule: Each jompus is sweet.
rule jompus_is_sweet:
    foreach facts.is_a($thing, "jompus", True)
    assert facts.is_sweet($thing, True)

# Rule: Jompuses are zumpuses.
rule jompus_is_zumpus:
    foreach facts.is_a($thing, "jompus", True)
    assert facts.is_a($thing, "zumpus", True)

# Rule: Each zumpus is brown.
rule zumpus_is_brown:
    foreach facts.is_a($thing, "zumpus", True)
    assert facts.is_brown($thing, True)

# Rule: Every zumpus is a yumpus.
rule zumpus_is_yumpus:
    foreach facts.is_a($thing, "zumpus", True)
    assert facts.is_a($thing, "yumpus", True)

# Query: Is Max not brown? (i.e., does is_brown("Max", False) hold?)
query facts.is_brown("Max", False)