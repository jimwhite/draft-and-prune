# Facts
facts.is_a("Sam", "wumpus", True)

# Rules
# Rule: Every yumpus is aggressive.
rule_yumpus_aggressive = foreach(
    facts.is_a(thing, "yumpus", True)
).assert_(
    facts.is_a(thing, "aggressive", True)
)

# Rule: Each yumpus is a wumpus.
rule_yumpus_wumpus = foreach(
    facts.is_a(thing, "yumpus", True)
).assert_(
    facts.is_a(thing, "wumpus", True)
)

# Rule: Every wumpus is bright.
rule_wumpus_bright = foreach(
    facts.is_a(thing, "wumpus", True)
).assert_(
    facts.is_a(thing, "bright", True)
)

# Rule: Each wumpus is a jompus.
rule_wumpus_jompus = foreach(
    facts.is_a(thing, "wumpus", True)
).assert_(
    facts.is_a(thing, "jompus", True)
)

# Rule: Every jompus is a vumpus.
rule_jompus_vumpus = foreach(
    facts.is_a(thing, "jompus", True)
).assert_(
    facts.is_a(thing, "vumpus", True)
)

# Rule: Each vumpus is orange.
rule_vumpus_orange = foreach(
    facts.is_a(thing, "vumpus", True)
).assert_(
    facts.is_a(thing, "orange", True)
)

# Rule: Every vumpus is an impus.
rule_vumpus_impus = foreach(
    facts.is_a(thing, "vumpus", True)
).assert_(
    facts.is_a(thing, "impus", True)
)

# Rule: Each impus is a zumpus.
rule_impus_zumpus = foreach(
    facts.is_a(thing, "impus", True)
).assert_(
    facts.is_a(thing, "zumpus", True)
)

# Rule: Every zumpus is fruity.
rule_zumpus_fruity = foreach(
    facts.is_a(thing, "zumpus", True)
).assert_(
    facts.is_a(thing, "fruity", True)
)

# Rule: Every zumpus is a numpus.
rule_zumpus_numpus = foreach(
    facts.is_a(thing, "zumpus", True)
).assert_(
    facts.is_a(thing, "numpus", True)
)

# Rule: Every numpus is sour.
rule_numpus_sour = foreach(
    facts.is_a(thing, "numpus", True)
).assert_(
    facts.is_a(thing, "sour", True)
)

# Rule: Numpuses are dumpuses.
rule_numpus_dumpus = foreach(
    facts.is_a(thing, "numpus", True)
).assert_(
    facts.is_a(thing, "dumpus", True)
)

# Additional rules for completeness (though not needed for this query):
# Rule: Tumpuses are yumpuses.
rule_tumpus_yumpus = foreach(
    facts.is_a(thing, "tumpus", True)
).assert_(
    facts.is_a(thing, "yumpus", True)
)

# Rule: Tumpuses are not small.
rule_tumpus_not_small = foreach(
    facts.is_a(thing, "tumpus", True)
).assert_(
    facts.is_not_small(thing, True)
)

# Rule: Jompuses are not liquid.
rule_jompus_not_liquid = foreach(
    facts.is_a(thing, "jompus", True)
).assert_(
    facts.is_not_liquid(thing, True)
)

# Rule: Every impus is not transparent.
rule_impus_not_transparent = foreach(
    facts.is_a(thing, "impus", True)
).assert_(
    facts.is_not_transparent(thing, True)
)

# Rule: Rompuses are not fruity.
rule_rompus_not_fruity = foreach(
    facts.is_a(thing, "rompus", True)
).assert_(
    facts.is_not_fruity(thing, True)
)

# Query
query_is_fruity = facts.is_a("Sam", "fruity", True)