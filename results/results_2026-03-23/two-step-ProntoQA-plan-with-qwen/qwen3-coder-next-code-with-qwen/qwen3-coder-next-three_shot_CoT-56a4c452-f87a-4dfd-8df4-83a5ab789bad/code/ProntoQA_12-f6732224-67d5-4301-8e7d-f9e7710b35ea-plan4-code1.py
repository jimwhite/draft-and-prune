# Facts
facts.is_a("Fae", "dumpus", True)

# Rules
# Rule: Each tumpus is orange.
rule.tumpus_is_orange
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_orange($thing, True)

# Rule: Tumpuses are numpuses.
rule.tumpus_is_numpus
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Numpuses are small.
rule.numpus_is_small
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_small($thing, True)

# Rule: Numpuses are vumpuses.
rule.numpus_is_vumpus
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Every vumpus is sour.
rule.vumpus_is_sour
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_sour($thing, True)

# Rule: Vumpuses are dumpuses.
rule.vumpus_is_dumpus
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "dumpus", True)

# Rule: Each dumpus is cold.
rule.dumpus_is_cold
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_cold($thing, True)

# Rule: Every dumpus is a zumpus.
rule.dumpus_is_zumpus
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Each zumpus is dull.
rule.zumpus_is_dull
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_dull($thing, True)

# Rule: Zumpuses are yumpuses.
rule.zumpus_is_yumpus
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Jompuses are floral.
rule.jompus_is_floral
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_floral($thing, True)

# Rule: Every yumpus is not amenable.
rule.yumpus_is_not_amenable
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_amenable($thing, False)

# Rule: Each yumpus is a rompus.
rule.yumpus_is_rompus
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "rompus", True)

# Rule: Every rompus is opaque.
rule.rompus_is_opaque
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_opaque($thing, True)

# Rule: Rompuses are impuses.
rule.rompus_is_impus
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "impus", True)

# Rule: Impuses are not floral.
rule.impus_is_not_floral
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_floral($thing, False)

# Rule: Impuses are wumpuses.
rule.impus_is_wumpus
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Query
query.fae_not_floral
    facts.is_floral("Fae", False)