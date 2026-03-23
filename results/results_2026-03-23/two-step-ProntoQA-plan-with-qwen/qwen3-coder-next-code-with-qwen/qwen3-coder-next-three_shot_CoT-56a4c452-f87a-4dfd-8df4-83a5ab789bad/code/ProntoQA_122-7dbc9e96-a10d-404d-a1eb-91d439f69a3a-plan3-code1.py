# Facts
facts.is_a("Fae", "numpus", True)

# Rules
# Rule: Rompuses are metallic.
rule rompus_is_metallic:
    foreach facts.is_a($thing, "rompus", True)
    assert facts.is_metallic($thing, True)

# Rule: Rompuses are dumpuses.
rule rompus_is_dumpus:
    foreach facts.is_a($thing, "rompus", True)
    assert facts.is_a($thing, "dumpus", True)

# Rule: Dumpuses are blue.
rule dumpus_is_blue:
    foreach facts.is_a($thing, "dumpus", True)
    assert facts.is_blue($thing, True)

# Rule: Every dumpus is a numpus.
rule dumpus_is_numpus:
    foreach facts.is_a($thing, "dumpus", True)
    assert facts.is_a($thing, "numpus", True)

# Rule: Every numpus is fruity.
rule numpus_is_fruity:
    foreach facts.is_a($thing, "numpus", True)
    assert facts.is_fruity($thing, True)

# Rule: Numpuses are jompuses.
rule numpus_is_jompus:
    foreach facts.is_a($thing, "numpus", True)
    assert facts.is_a($thing, "jompus", True)

# Rule: Every jompus is mean.
rule jompus_is_mean:
    foreach facts.is_a($thing, "jompus", True)
    assert facts.is_mean($thing, True)

# Rule: Jompuses are tumpuses.
rule jompus_is_tumpus:
    foreach facts.is_a($thing, "jompus", True)
    assert facts.is_a($thing, "tumpus", True)

# Rule: Tumpuses are not temperate.
rule tumpus_is_not_temperate:
    foreach facts.is_a($thing, "tumpus", True)
    assert facts.is_temperate($thing, False)

# Rule: Tumpuses are impuses.
rule tumpus_is_impus:
    foreach facts.is_a($thing, "tumpus", True)
    assert facts.is_a($thing, "impus", True)

# Rule: Impuses are not dull.
rule impus_is_not_dull:
    foreach facts.is_a($thing, "impus", True)
    assert facts.is_dull($thing, False)

# Rule: Each impus is a yumpus.
rule impus_is_yumpus:
    foreach facts.is_a($thing, "impus", True)
    assert facts.is_a($thing, "yumpus", True)

# Rule: Every yumpus is not transparent.
rule yumpus_is_not_transparent:
    foreach facts.is_a($thing, "yumpus", True)
    assert facts.is_transparent($thing, False)

# Rule: Yumpuses are zumpuses.
rule yumpus_is_zumpus:
    foreach facts.is_a($thing, "yumpus", True)
    assert facts.is_a($thing, "zumpus", True)

# Rule: Wumpuses are transparent.
rule wumpus_is_transparent:
    foreach facts.is_a($thing, "wumpus", True)
    assert facts.is_transparent($thing, True)

# Rule: Zumpuses are not sweet.
rule zumpus_is_not_sweet:
    foreach facts.is_a($thing, "zumpus", True)
    assert facts.is_sweet($thing, False)

# Rule: Zumpuses are vumpuses.
rule zumpus_is_vumpus:
    foreach facts.is_a($thing, "zumpus", True)
    assert facts.is_a($thing, "vumpus", True)

# Query
query facts.is_transparent("Fae", False)