# Facts
facts.is_a("Wren", "yumpus", True)

# Rules
# Rule: Every jompus is bright.
rule1 = foreach(
    facts.is_a($thing, "jompus", True)
).assert_(
    facts.is_bright($thing, True)
)

# Rule: Every jompus is a vumpus.
rule2 = foreach(
    facts.is_a($thing, "jompus", True)
).assert_(
    facts.is_a($thing, "vumpus", True)
)

# Rule: Vumpuses are floral.
rule3 = foreach(
    facts.is_a($thing, "vumpus", True)
).assert_(
    facts.is_floral($thing, True)
)

# Rule: Every vumpus is a yumpus.
rule4 = foreach(
    facts.is_a($thing, "vumpus", True)
).assert_(
    facts.is_a($thing, "yumpus", True)
)

# Rule: Every yumpus is not temperate.
rule5 = foreach(
    facts.is_a($thing, "yumpus", True)
).assert_(
    facts.is_temperate($thing, False)
)

# Rule: Each yumpus is a numpus.
rule6 = foreach(
    facts.is_a($thing, "yumpus", True)
).assert_(
    facts.is_a($thing, "numpus", True)
)

# Rule: Every numpus is sweet.
rule7 = foreach(
    facts.is_a($thing, "numpus", True)
).assert_(
    facts.is_sweet($thing, True)
)

# Rule: Each numpus is a zumpus.
rule8 = foreach(
    facts.is_a($thing, "numpus", True)
).assert_(
    facts.is_a($thing, "zumpus", True)
)

# Rule: Zumpuses are mean.
rule9 = foreach(
    facts.is_a($thing, "zumpus", True)
).assert_(
    facts.is_mean($thing, True)
)

# Rule: Zumpuses are rompuses.
rule10 = foreach(
    facts.is_a($thing, "zumpus", True)
).assert_(
    facts.is_a($thing, "rompus", True)
)

# Rule: Each rompus is not feisty.
rule11 = foreach(
    facts.is_a($thing, "rompus", True)
).assert_(
    facts.is_feisty($thing, False)
)

# Rule: Every impus is not transparent.
rule12 = foreach(
    facts.is_a($thing, "impus", True)
).assert_(
    facts.is_transparent($thing, False)
)

# Rule: Each rompus is a wumpus.
rule13 = foreach(
    facts.is_a($thing, "rompus", True)
).assert_(
    facts.is_a($thing, "wumpus", True)
)

# Rule: Wumpuses are transparent.
rule14 = foreach(
    facts.is_a($thing, "wumpus", True)
).assert_(
    facts.is_transparent($thing, True)
)

# Rule: Each wumpus is a dumpus.
rule15 = foreach(
    facts.is_a($thing, "wumpus", True)
).assert_(
    facts.is_a($thing, "dumpus", True)
)

# Rule: Dumpuses are large.
rule16 = foreach(
    facts.is_a($thing, "dumpus", True)
).assert_(
    facts.is_large($thing, True)
)

# Rule: Each dumpus is a tumpus.
rule17 = foreach(
    facts.is_a($thing, "dumpus", True)
).assert_(
    facts.is_a($thing, "tumpus", True)
)

# Query
query_result = facts.is_transparent("Wren", True)