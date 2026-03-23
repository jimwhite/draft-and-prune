# Facts
facts.is_a("Wren", "vumpus", True)

# Rules
# Rule: Tumpuses are dull.
tumpus_is_dull
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_dull($thing, True)

# Rule: Tumpuses are jompuses.
tumpus_is_jompus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Rule: Jompuses are not sour.
jompus_is_not_sour
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_sour($thing, False)

# Rule: Each jompus is a vumpus.
jompus_is_vumpus
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Vumpuses are feisty.
vumpus_is_feisty
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_feisty($thing, True)

# Rule: Vumpuses are dumpuses.
vumpus_is_dumpus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "dumpus", True)

# Rule: Dumpuses are cold.
dumpus_is_cold
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_cold($thing, True)

# Rule: Each dumpus is a yumpus.
dumpus_is_yumpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Each yumpus is transparent.
yumpus_is_transparent
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_transparent($thing, True)

# Rule: Each yumpus is a numpus.
yumpus_is_numpus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Numpuses are not amenable.
numpus_is_not_amenable
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_amenable($thing, False)

# Rule: Numpuses are zumpuses.
numpus_is_zumpus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Each zumpus is orange.
zumpus_is_orange
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_orange($thing, True)

# Rule: Each zumpus is a rompus.
zumpus_is_rompus
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "rompus", True)

# Rule: Rompuses are earthy.
rompus_is_earthy
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_earthy($thing, True)

# Rule: Each impus is not orange.
impus_is_not_orange
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_orange($thing, False)

# Rule: Rompuses are wumpuses.
rompus_is_wumpus
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Query: Is Wren not orange?
query
    facts.is_orange("Wren", False)