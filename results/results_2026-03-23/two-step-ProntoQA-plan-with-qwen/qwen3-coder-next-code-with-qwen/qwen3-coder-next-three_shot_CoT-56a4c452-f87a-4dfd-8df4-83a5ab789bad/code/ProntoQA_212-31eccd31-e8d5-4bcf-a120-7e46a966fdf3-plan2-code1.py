# Facts
facts.is_a("Stella", "wumpus", True)

# Rules
# Rule: Every tumpus is red.
rule.tumpus_is_red
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_red($thing, True)

# Rule: Each tumpus is a wumpus.
rule.tumpus_is_wumpus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Every wumpus is sweet.
rule.wumpus_is_sweet
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_sweet($thing, True)

# Rule: Wumpuses are vumpuses.
rule.wumpus_is_vumpus
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Vumpuses are small.
rule.vumpus_is_small
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_small($thing, True)

# Rule: Every vumpus is a jompus.
rule.vumpus_is_jompus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Rule: Every jompus is not aggressive.
rule.jompus_is_not_aggressive
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_aggressive($thing, False)

# Rule: Zumpuses are temperate.
rule.zumpus_is_temperate
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_temperate($thing, True)

# Rule: Each jompus is a dumpus.
rule.jompus_is_dumpus
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "dumpus", True)

# Rule: Each dumpus is bright.
rule.dumpus_is_bright
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_bright($thing, True)

# Rule: Every dumpus is a numpus.
rule.dumpus_is_numpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Numpuses are not temperate.
rule.numpus_is_not_temperate
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_temperate($thing, False)

# Rule: Numpuses are rompuses.
rule.numpus_is_rompus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "rompus", True)

# Rule: Each rompus is not luminous.
rule.rompus_is_not_luminous
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_luminous($thing, False)

# Rule: Every rompus is a yumpus.
rule.rompus_is_yumpus
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Yumpuses are opaque.
rule.yumpus_is_opaque
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_opaque($thing, True)

# Rule: Every yumpus is an impus.
rule.yumpus_is_impus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "impus", True)

# Query
query_result = facts.is_temperate("Stella", False)