# Facts:
facts.is_a("Wren", "numpus", True)

# Rules:
# Rule: Each dumpus is a yumpus.
dumpus_is_yumpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Yumpuses are transparent.
yumpus_is_transparent
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_transparent($thing, True)

# Rule: Each rompus is not mean.
rompus_is_not_mean
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_mean($thing, False)

# Rule: Yumpuses are vumpuses.
yumpus_is_vumpus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Vumpuses are not brown.
vumpus_is_not_brown
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_brown($thing, False)

# Rule: Vumpuses are numpuses.
vumpus_is_numpus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Numpuses are not temperate.
numpus_is_not_temperate
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_temperate($thing, False)

# Rule: Every numpus is a zumpus.
numpus_is_zumpus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Each zumpus is bitter.
zumpus_is_bitter
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_bitter($thing, True)

# Rule: Zumpuses are tumpuses.
zumpus_is_tumpus
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "tumpus", True)

# Rule: Tumpuses are shy.
tumpus_is_shy
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_shy($thing, True)

# Rule: Tumpuses are impuses.
tumpus_is_impus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "impus", True)

# Rule: Impuses are wooden.
impus_is_wooden
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_wooden($thing, True)

# Rule: Each impus is a wumpus.
impus_is_wumpus
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Each wumpus is mean.
wumpus_is_mean
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_mean($thing, True)

# Rule: Every wumpus is a jompus.
wumpus_is_jompus
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Query:
facts.is_mean("Wren", False)