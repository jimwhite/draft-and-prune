Facts:
facts.is_a("Sam", "wumpus", True)

Rules:
# Rule: Tumpuses are not small.
tumpus_is_not_small
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_small($thing, False)

# Rule: Tumpuses are yumpuses.
tumpus_is_yumpus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Every yumpus is aggressive.
yumpus_is_aggressive
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_aggressive($thing, True)

# Rule: Each yumpus is a wumpus.
yumpus_is_wumpus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Every wumpus is bright.
wumpus_is_bright
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_bright($thing, True)

# Rule: Each wumpus is a jompus.
wumpus_is_jompus
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Rule: Jompuses are not liquid.
jompus_is_not_liquid
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_liquid($thing, False)

# Rule: Every jompus is a vumpus.
jompus_is_vumpus
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Each vumpus is orange.
vumpus_is_orange
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_orange($thing, True)

# Rule: Every vumpus is an impus.
vumpus_is_impus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "impus", True)

# Rule: Every impus is not transparent.
impus_is_not_transparent
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_transparent($thing, False)

# Rule: Each impus is a zumpus.
impus_is_zumpus
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Every zumpus is fruity.
zumpus_is_fruity
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_fruity($thing, True)

# Rule: Every zumpus is a numpus.
zumpus_is_numpus
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Every numpus is sour.
numpus_is_sour
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_sour($thing, True)

# Rule: Rompuses are not fruity.
rompus_is_not_fruity
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_fruity($thing, False)

# Rule: Numpuses are dumpuses.
numpus_is_dumpus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "dumpus", True)

Query:
facts.is_fruity("Sam", True)