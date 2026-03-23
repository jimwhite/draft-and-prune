# Facts
facts.is_a("Sam", "numpus", True)

# Rules
# Rule: Tumpuses are fruity.
tumpus_is_fruity
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_fruity($thing, True)

# Rule: Tumpuses are dumpuses.
tumpus_is_dumpus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "dumpus", True)

# Rule: Each dumpus is liquid.
dumpus_is_liquid
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_liquid($thing, True)

# Rule: Each dumpus is a numpus.
dumpus_is_numpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Numpuses are sour.
numpus_is_sour
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_sour($thing, True)

# Rule: Numpuses are jompuses.
numpus_is_jompus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Rule: Jompuses are not cold.
jompus_is_not_cold
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_cold($thing, False)

# Rule: Jompuses are wumpuses.
jompus_is_wumpus
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Wumpuses are brown.
wumpus_is_brown
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_brown($thing, True)

# Rule: Wumpuses are vumpuses.
wumpus_is_vumpus
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Vumpuses are happy.
vumpus_is_happy
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_happy($thing, True)

# Rule: Each vumpus is a yumpus.
vumpus_is_yumpus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Each yumpus is large.
yumpus_is_large
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_large($thing, True)

# Rule: Each yumpus is a rompus.
yumpus_is_rompus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "rompus", True)

# Rule: Rompuses are not mean.
rompus_is_not_mean
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_mean($thing, False)

# Rule: Every rompus is a zumpus.
rompus_is_zumpus
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Each impus is not large.
impus_is_not_large
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_large($thing, False)

# Query: Is Sam large?
query_result = knowledge_engine.ask("facts.is_large", "Sam", True)