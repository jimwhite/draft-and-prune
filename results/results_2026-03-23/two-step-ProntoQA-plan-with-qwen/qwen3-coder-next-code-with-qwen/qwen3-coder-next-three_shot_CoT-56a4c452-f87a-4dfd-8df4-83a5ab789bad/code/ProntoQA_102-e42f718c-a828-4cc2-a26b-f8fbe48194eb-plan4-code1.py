Facts:
facts.is_a("Rex", "wumpus", True)

Rules:
# Rule: Each dumpus is not dull.
dumpus_is_not_dull
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_dull($thing, False)

# Rule: Tumpuses are not spicy.
tumpus_is_not_spicy
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_spicy($thing, False)

# Rule: Dumpuses are vumpuses.
dumpus_is_vumpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Vumpuses are fruity.
vumpus_is_fruity
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_fruity($thing, True)

# Rule: Each vumpus is a zumpus.
vumpus_is_zumpus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Each zumpus is large.
zumpus_is_large
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_large($thing, True)

# Rule: Each zumpus is a wumpus.
zumpus_is_wumpus
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Wumpuses are blue.
wumpus_is_blue
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_blue($thing, True)

# Rule: Wumpuses are numpuses.
wumpus_is_numpus
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Each numpus is kind.
numpus_is_kind
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_kind($thing, True)

# Rule: Numpuses are rompuses.
numpus_is_rompus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "rompus", True)

# Rule: Rompuses are cold.
rompus_is_cold
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_cold($thing, True)

# Rule: Rompuses are jompuses.
rompus_is_jompus
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Rule: Jompuses are not transparent.
jompus_is_not_transparent
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_transparent($thing, False)

# Rule: Jompuses are yumpuses.
jompus_is_yumpus
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Yumpuses are spicy.
yumpus_is_spicy
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_spicy($thing, True)

# Rule: Every yumpus is an impus.
yumpus_is_impus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "impus", True)

Query:
facts.is_spicy("Rex", False)